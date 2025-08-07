"""
Analyseur audio en temps réel pour la réactivité musicale.
"""

import numpy as np
import threading
import queue

# Audio processing imports (optional - will gracefully degrade if not available)
try:
    import pyaudio
    import scipy.signal
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("Audio libraries not available. Install pyaudio and scipy for music reactivity:")
    print("pip install pyaudio scipy")


class AudioAnalyzer:
    """
    Analyseur audio en temps réel pour la réactivité musicale.
    
    Capture l'audio du microphone et extrait les caractéristiques fréquentielles
    pour contrôler les paramètres visuels.
    """
    
    def __init__(self, sample_rate: int = 44100, chunk_size: int = 1024):
        """
        Initialise l'analyseur audio.
        
        Args:
            sample_rate: Fréquence d'échantillonnage audio
            chunk_size: Taille des blocs audio à analyser
        """
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.audio_queue = queue.Queue()
        self.is_running = False
        self.audio_thread = None
        
        # Paramètres d'analyse
        self.bass_range = (20, 250)      # Hz
        self.mid_range = (250, 4000)     # Hz  
        self.high_range = (4000, 20000)  # Hz
        
        # Variables de sortie (thread-safe)
        self.bass_level = 0.0
        self.mid_level = 0.0
        self.high_level = 0.0
        self.overall_volume = 0.0
        self.beat_detected = False
        
        # Historique pour la détection de beats
        self.volume_history = []
        self.beat_threshold = 1.3
        self.beat_cooldown = 0
        
        # Lissage des valeurs
        self.smoothing_factor = 0.8
        
        # PyAudio setup
        if AUDIO_AVAILABLE:
            self.pa = pyaudio.PyAudio()
            self.stream = None
        else:
            self.pa = None
            self.stream = None
    
    def start_audio_capture(self):
        """Démarre la capture audio en arrière-plan"""
        if not AUDIO_AVAILABLE:
            print("Audio non disponible - mode silencieux")
            return False
            
        try:
            self.stream = self.pa.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                stream_callback=self._audio_callback
            )
            
            self.is_running = True
            self.audio_thread = threading.Thread(target=self._process_audio, daemon=True)
            self.audio_thread.start()
            
            print("🎵 Capture audio démarrée - Votre art réagit maintenant à la musique!")
            return True
            
        except Exception as e:
            print(f"Erreur audio: {e}")
            return False
    
    def stop_audio_capture(self):
        """Arrête la capture audio"""
        self.is_running = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
        if self.pa:
            self.pa.terminate()
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Callback pour recevoir les données audio"""
        try:
            audio_data = np.frombuffer(in_data, dtype=np.float32)
            self.audio_queue.put(audio_data, block=False)
        except queue.Full:
            pass  # Skip if queue is full
        return (None, pyaudio.paContinue)
    
    def _process_audio(self):
        """Thread principal de traitement audio"""
        while self.is_running:
            try:
                # Récupérer les données audio
                audio_data = self.audio_queue.get(timeout=0.1)
                
                # Calculer la FFT
                fft = np.fft.rfft(audio_data)
                magnitude = np.abs(fft)
                
                # Créer l'échelle de fréquences
                freqs = np.fft.rfftfreq(len(audio_data), 1/self.sample_rate)
                
                # Extraire les niveaux par bande de fréquence
                bass_indices = np.where((freqs >= self.bass_range[0]) & (freqs <= self.bass_range[1]))
                mid_indices = np.where((freqs >= self.mid_range[0]) & (freqs <= self.mid_range[1]))
                high_indices = np.where((freqs >= self.high_range[0]) & (freqs <= self.high_range[1]))
                
                # Calculer les niveaux moyens (avec lissage)
                bass_new = np.mean(magnitude[bass_indices]) if len(bass_indices[0]) > 0 else 0
                mid_new = np.mean(magnitude[mid_indices]) if len(mid_indices[0]) > 0 else 0
                high_new = np.mean(magnitude[high_indices]) if len(high_indices[0]) > 0 else 0
                volume_new = np.mean(magnitude)
                
                # Appliquer le lissage
                self.bass_level = self.bass_level * self.smoothing_factor + bass_new * (1 - self.smoothing_factor)
                self.mid_level = self.mid_level * self.smoothing_factor + mid_new * (1 - self.smoothing_factor)
                self.high_level = self.high_level * self.smoothing_factor + high_new * (1 - self.smoothing_factor)
                self.overall_volume = self.overall_volume * self.smoothing_factor + volume_new * (1 - self.smoothing_factor)
                
                # Détection de beats
                self._detect_beat(volume_new)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Erreur traitement audio: {e}")
                continue
    
    def _detect_beat(self, current_volume):
        """Détecte les beats dans l'audio"""
        self.volume_history.append(current_volume)
        
        # Garder seulement les 20 dernières valeurs
        if len(self.volume_history) > 20:
            self.volume_history.pop(0)
        
        # Réduire le cooldown
        if self.beat_cooldown > 0:
            self.beat_cooldown -= 1
        
        # Détecter un beat si le volume actuel dépasse significativement la moyenne récente
        if len(self.volume_history) >= 10 and self.beat_cooldown == 0:
            recent_avg = np.mean(self.volume_history[:-5])  # Moyenne des valeurs récentes
            if current_volume > recent_avg * self.beat_threshold:
                self.beat_detected = True
                self.beat_cooldown = 10  # Cooldown pour éviter les faux positifs
                return
        
        self.beat_detected = False
    
    def get_audio_features(self) -> dict:
        """
        Retourne les caractéristiques audio actuelles.
        
        Returns:
            Dict avec bass_level, mid_level, high_level, overall_volume, beat_detected
        """
        return {
            'bass_level': min(self.bass_level * 100, 1.0),      # Normalisé 0-1
            'mid_level': min(self.mid_level * 50, 1.0),         # Normalisé 0-1  
            'high_level': min(self.high_level * 20, 1.0),       # Normalisé 0-1
            'overall_volume': min(self.overall_volume * 30, 1.0), # Normalisé 0-1
            'beat_detected': self.beat_detected
        }