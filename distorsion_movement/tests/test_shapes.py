"""
Tests unitaires pour le module de rendu de formes.
"""

import pytest
import pygame
import math
from unittest.mock import Mock, patch, MagicMock

from distorsion_movement.shapes import ShapeRenderer, get_shape_renderer_function


@pytest.fixture
def mock_surface():
    """Crée une surface pygame mockée pour les tests."""
    surface = Mock()
    surface.get_width.return_value = 800
    surface.get_height.return_value = 600
    return surface


class TestShapeRenderer:
    """Tests pour la classe ShapeRenderer."""
    
    def test_rotate_points_no_rotation(self):
        """Test de rotation avec angle zéro."""
        points = [(10, 0), (0, 10), (-10, 0), (0, -10)]
        result = ShapeRenderer._rotate_points(points, 0, 100, 100)
        
        expected = [(110, 100), (100, 110), (90, 100), (100, 90)]
        assert result == expected
    
    def test_rotate_points_90_degrees(self):
        """Test de rotation de 90 degrés."""
        points = [(10, 0), (0, 10)]
        result = ShapeRenderer._rotate_points(points, math.pi/2, 0, 0)
        
        # Après rotation de 90°: (10,0) -> (0,10), (0,10) -> (-10,0)
        expected = [(0, 10), (-10, 0)]
        assert result == expected
    
    def test_rotate_points_with_invalid_coordinates(self):
        """Test de gestion des coordonnées invalides."""
        points = [(float('inf'), 0), (0, float('nan'))]
        result = ShapeRenderer._rotate_points(points, 0, 50, 50)
        
        # Coordonnées invalides doivent être remplacées par le centre
        expected = [(50, 50), (50, 50)]
        assert result == expected
    
    @patch('pygame.draw.polygon')
    def test_draw_square_success(self, mock_polygon, mock_surface):
        """Test du dessin d'un carré réussi."""
        ShapeRenderer.draw_square(mock_surface, 100, 100, 0, 20, (255, 0, 0))
        
        # Vérifier que pygame.draw.polygon a été appelé
        mock_polygon.assert_called_once()
        args = mock_polygon.call_args[0]
        assert args[0] == mock_surface  # surface
        assert args[1] == (255, 0, 0)   # couleur
        assert len(args[2]) == 4        # 4 coins pour un carré
    
    @patch('pygame.draw.rect')
    @patch('pygame.draw.polygon', side_effect=ValueError("Invalid polygon"))
    def test_draw_square_fallback(self, mock_polygon, mock_rect, mock_surface):
        """Test du fallback en cas d'erreur lors du dessin d'un carré."""
        ShapeRenderer.draw_square(mock_surface, 100, 100, 0, 20, (255, 0, 0))
        
        # Vérifier que le fallback (rectangle) a été utilisé
        mock_polygon.assert_called_once()
        mock_rect.assert_called_once()
    
    @patch('pygame.draw.circle')
    def test_draw_circle_success(self, mock_circle, mock_surface):
        """Test du dessin d'un cercle réussi."""
        ShapeRenderer.draw_circle(mock_surface, 100, 100, 0, 20, (0, 255, 0))
        
        # Vérifier que pygame.draw.circle a été appelé avec les bons paramètres
        mock_circle.assert_called_once_with(mock_surface, (0, 255, 0), (100, 100), 10)
    
    @patch('pygame.draw.rect')
    @patch('pygame.draw.circle', side_effect=ValueError("Invalid circle"))
    def test_draw_circle_fallback(self, mock_circle, mock_rect, mock_surface):
        """Test du fallback en cas d'erreur lors du dessin d'un cercle."""
        ShapeRenderer.draw_circle(mock_surface, 100, 100, 0, 20, (0, 255, 0))
        
        # Vérifier que le fallback (rectangle) a été utilisé
        mock_circle.assert_called_once()
        mock_rect.assert_called_once()
    
    @patch('pygame.draw.polygon')
    def test_draw_triangle_success(self, mock_polygon, mock_surface):
        """Test du dessin d'un triangle réussi."""
        ShapeRenderer.draw_triangle(mock_surface, 100, 100, 0, 30, (0, 0, 255))
        
        # Vérifier que pygame.draw.polygon a été appelé
        mock_polygon.assert_called_once()
        args = mock_polygon.call_args[0]
        assert args[0] == mock_surface  # surface
        assert args[1] == (0, 0, 255)   # couleur
        assert len(args[2]) == 3        # 3 coins pour un triangle
    
    @patch('pygame.draw.polygon')
    def test_draw_hexagon_success(self, mock_polygon, mock_surface):
        """Test du dessin d'un hexagone réussi."""
        ShapeRenderer.draw_hexagon(mock_surface, 100, 100, 0, 24, (255, 255, 0))
        
        # Vérifier que pygame.draw.polygon a été appelé
        mock_polygon.assert_called_once()
        args = mock_polygon.call_args[0]
        assert args[0] == mock_surface  # surface
        assert args[1] == (255, 255, 0) # couleur
        assert len(args[2]) == 6        # 6 coins pour un hexagone
    
    @patch('pygame.draw.polygon')
    def test_draw_pentagon_success(self, mock_polygon, mock_surface):
        """Test du dessin d'un pentagone réussi."""
        ShapeRenderer.draw_pentagon(mock_surface, 100, 100, 0, 25, (255, 0, 255))
        
        # Vérifier que pygame.draw.polygon a été appelé
        mock_polygon.assert_called_once()
        args = mock_polygon.call_args[0]
        assert args[0] == mock_surface  # surface
        assert args[1] == (255, 0, 255) # couleur
        assert len(args[2]) == 5        # 5 coins pour un pentagone
    
    @patch('pygame.draw.polygon')
    def test_draw_star_success(self, mock_polygon, mock_surface):
        """Test du dessin d'une étoile réussie."""
        ShapeRenderer.draw_star(mock_surface, 100, 100, 0, 30, (128, 128, 128))
        
        # Vérifier que pygame.draw.polygon a été appelé
        mock_polygon.assert_called_once()
        args = mock_polygon.call_args[0]
        assert args[0] == mock_surface  # surface
        assert args[1] == (128, 128, 128) # couleur
        assert len(args[2]) == 10       # 10 points pour une étoile (5 externes + 5 internes)
    
    @patch('pygame.draw.polygon')
    def test_draw_diamond_success(self, mock_polygon, mock_surface):
        """Test du dessin d'un losange réussi."""
        ShapeRenderer.draw_diamond(mock_surface, 100, 100, 0, 20, (64, 64, 64))
        
        # Vérifier que pygame.draw.polygon a été appelé
        mock_polygon.assert_called_once()
        args = mock_polygon.call_args[0]
        assert args[0] == mock_surface  # surface
        assert args[1] == (64, 64, 64)  # couleur
        assert len(args[2]) == 4        # 4 coins pour un losange
    
    @patch('pygame.draw.polygon')
    def test_draw_square_with_rotation(self, mock_polygon, mock_surface):
        """Test du dessin d'un carré avec rotation."""
        rotation = math.pi / 4  # 45 degrés
        ShapeRenderer.draw_square(mock_surface, 100, 100, rotation, 20, (255, 0, 0))
        
        # Vérifier que pygame.draw.polygon a été appelé
        mock_polygon.assert_called_once()
        args = mock_polygon.call_args[0]
        
        # Les points doivent être différents de ceux sans rotation
        rotated_points = args[2]
        assert len(rotated_points) == 4
        
        # Vérifier que les points ne sont pas aux positions "normales" d'un carré
        # (ça confirme que la rotation a été appliquée)
        expected_unrotated = [(90, 90), (110, 90), (110, 110), (90, 110)]
        assert rotated_points != expected_unrotated
    
    def test_draw_with_zero_size(self, mock_surface):
        """Test du comportement avec une taille nulle."""
        with patch('pygame.draw.circle') as mock_circle:
            ShapeRenderer.draw_circle(mock_surface, 100, 100, 0, 0, (255, 0, 0))
            # Le rayon doit être au minimum 1
            mock_circle.assert_called_once_with(mock_surface, (255, 0, 0), (100, 100), 1)
    
    def test_draw_with_negative_size(self, mock_surface):
        """Test du comportement avec une taille négative."""
        with patch('pygame.draw.circle') as mock_circle:
            ShapeRenderer.draw_circle(mock_surface, 100, 100, 0, -10, (255, 0, 0))
            # Le rayon doit être au minimum 1
            mock_circle.assert_called_once_with(mock_surface, (255, 0, 0), (100, 100), 1)


class TestShapeRendererFunctionGetter:
    """Tests pour la fonction get_shape_renderer_function."""
    
    def test_get_square_function(self):
        """Test de récupération de la fonction carré."""
        func = get_shape_renderer_function("square")
        assert func == ShapeRenderer.draw_square
    
    def test_get_circle_function(self):
        """Test de récupération de la fonction cercle."""
        func = get_shape_renderer_function("circle")
        assert func == ShapeRenderer.draw_circle
    
    def test_get_triangle_function(self):
        """Test de récupération de la fonction triangle."""
        func = get_shape_renderer_function("triangle")
        assert func == ShapeRenderer.draw_triangle
    
    def test_get_hexagon_function(self):
        """Test de récupération de la fonction hexagone."""
        func = get_shape_renderer_function("hexagon")
        assert func == ShapeRenderer.draw_hexagon
    
    def test_get_pentagon_function(self):
        """Test de récupération de la fonction pentagone."""
        func = get_shape_renderer_function("pentagon")
        assert func == ShapeRenderer.draw_pentagon
    
    def test_get_star_function(self):
        """Test de récupération de la fonction étoile."""
        func = get_shape_renderer_function("star")
        assert func == ShapeRenderer.draw_star
    
    def test_get_diamond_function(self):
        """Test de récupération de la fonction losange."""
        func = get_shape_renderer_function("diamond")
        assert func == ShapeRenderer.draw_diamond
    
    def test_get_unknown_function_returns_square(self):
        """Test que les formes inconnues retournent la fonction carré par défaut."""
        func = get_shape_renderer_function("unknown_shape")
        assert func == ShapeRenderer.draw_square
    
    def test_get_empty_string_returns_square(self):
        """Test que chaîne vide retourne la fonction carré par défaut."""
        func = get_shape_renderer_function("")
        assert func == ShapeRenderer.draw_square
    
    def test_get_none_returns_square(self):
        """Test que None retourne la fonction carré par défaut."""
        func = get_shape_renderer_function(None)
        assert func == ShapeRenderer.draw_square


@pytest.mark.integration
class TestShapeIntegration:
    """Tests d'intégration pour les formes."""
    
    @patch('pygame.draw.polygon')
    @patch('pygame.draw.circle')
    @patch('pygame.draw.rect')
    def test_all_shapes_can_be_drawn(self, mock_rect, mock_circle, mock_polygon, mock_surface):
        """Test que toutes les formes peuvent être dessinées sans erreur."""
        shapes = ["square", "circle", "triangle", "hexagon", "pentagon", "star", "diamond"]
        
        for shape_type in shapes:
            func = get_shape_renderer_function(shape_type)
            # Ne doit pas lever d'exception
            try:
                func(mock_surface, 100, 100, 0, 20, (255, 255, 255))
            except Exception as e:
                pytest.fail(f"La forme {shape_type} a levé une exception: {e}")
    
    @patch('pygame.draw.polygon')
    @patch('pygame.draw.circle')
    @patch('pygame.draw.rect')
    def test_shapes_with_various_parameters(self, mock_rect, mock_circle, mock_polygon, mock_surface):
        """Test des formes avec différents paramètres."""
        test_cases = [
            (50, 50, 0, 10, (255, 0, 0)),
            (200, 150, math.pi/2, 30, (0, 255, 0)),
            (0, 0, math.pi, 5, (0, 0, 255)),
            (1000, 1000, 2*math.pi, 50, (255, 255, 255)),
        ]
        
        for x, y, rotation, size, color in test_cases:
            for shape_type in ["square", "circle", "triangle", "star"]:
                func = get_shape_renderer_function(shape_type)
                # Ne doit pas lever d'exception
                try:
                    func(mock_surface, x, y, rotation, size, color)
                except Exception as e:
                    pytest.fail(f"Paramètres ({x}, {y}, {rotation}, {size}, {color}) "
                              f"ont causé une erreur pour {shape_type}: {e}")