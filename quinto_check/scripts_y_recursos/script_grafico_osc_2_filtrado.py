import numpy as np
import matplotlib.pyplot as plt

# Intentar importar scipy; si no está, algunos métodos no estarán disponibles
try:
    from scipy.signal import savgol_filter, butter, filtfilt, medfilt
    SCIPY_AVAILABLE = True
except Exception:
    SCIPY_AVAILABLE = False

# =========================
# === CONFIGURACIÓN ===
# =========================
archivo = "ripple_buc.csv"

# Ventana temporal (opcional) - definen recorte sobre tiempo original
t_inicio = 0.0        # segundos, el nuevo "cero" será t_inicio si se usa desplazamiento (igual que antes)
t_fin = 60e-6          # segundos, None = sin recorte por final

# Método de despike: 'median', 'moving_average', 'savitzky_golay', 'hampel', 'butterworth'
method = "median"

# Parámetros por método (ajustalos según veas)
params = {
    "median_window_ms": 0.00015,       # ventana de la mediana en ms (para archivos con sampling_rate alto)
    "moving_avg_ms": 0.02,          # ventana media móvil en ms
    "savgol_window_ms": 0.05,       # ventana savgol en ms (debe ser impar en muestras)
    "savgol_poly": 3,
    "hampel_window_ms": 0.02,       # ventana del hampel en ms
    "hampel_n_sigma": 3,            # umbral sigma para considerar outlier
    "butter_order": 4,
    "butter_cutoff_khz": 50.0,      # corte en kHz (ajustá según tu señal)
}

# Si querés convertir unidades (ej: mV -> V)
force_unit_to_volt = True   # si el archivo dice mv, lo convierte; si no declara unidad, no toca

# =========================
# === LECTURA DEL ARCHIVO ===
# =========================
with open(archivo, "r") as f:
    lineas = f.readlines()

time_base = None
sampling_rate = None
data_unit = None
datos_raw = []

for linea in lineas:
    l = linea.strip()
    if l.startswith("Time Base:"):
        valor = l.split(":", 1)[1].strip()
        # soporta μs, ms, s
        if valor.endswith("μs"):
            time_base = float(valor[:-2]) * 1e-6
        elif valor.endswith("us"):  # por si no usan μ
            time_base = float(valor[:-2]) * 1e-6
        elif valor.endswith("ms"):
            time_base = float(valor[:-2]) * 1e-3
        elif valor.endswith("s"):
            time_base = float(valor[:-1])
    elif l.startswith("Sampling Rate:"):
        valor = l.split(":", 1)[1].strip()
        # ejemplos: 500MSa/s, 1GSa/s, 100kSa/s
        if "MSa" in valor:
            sampling_rate = float(valor.replace("MSa/s","").strip()) * 1e6
        elif "GSa" in valor:
            sampling_rate = float(valor.replace("GSa/s","").strip()) * 1e9
        elif "kSa" in valor:
            sampling_rate = float(valor.replace("kSa/s","").strip()) * 1e3
        else:
            # intento simple: extraer dígitos
            try:
                sampling_rate = float(''.join(ch for ch in valor if (ch.isdigit() or ch=='.'))) 
            except:
                sampling_rate = None
    elif l.lower().startswith("data unit:") or l.lower().startswith("data uint:"):
        data_unit = l.split(":",1)[1].strip().lower()
    else:
        # intentar parsear número (admite formatos tipo -9.20E+00)
        try:
            datos_raw.append(float(l))
        except:
            pass

datos = np.array(datos_raw)
if datos.size == 0:
    raise ValueError("No se encontraron datos numéricos en el archivo.")

# Conversión de unidades si corresponde
if force_unit_to_volt and data_unit is not None:
    if "mv" in data_unit:
        datos = datos / 1000.0
    # si viene en uV, etc. se podría agregar

# ===== vector de tiempo (por sampling_rate si disponible) =====
if sampling_rate is None:
    # si no hay sampling_rate, intentar usar Time Base (menos preciso)
    if time_base is None:
        raise ValueError("No pude determinar sampling_rate ni Time Base del archivo.")
    # time_base es el ancho total de la pantalla? No siempre. Asumimos que time_base corresponde al intervalo total.
    # Si no estás seguro, mejor definir sampling_rate a mano.
    N = len(datos)
    Ts = time_base / N
else:
    Ts = 1.0 / sampling_rate

N = len(datos)
t = np.arange(N) * Ts   # tiempo desde 0

# ===== desplazar cero y recortar por t_inicio/t_fin =====
t_shift = t - t_inicio
mask = t_shift >= 0
if t_fin is not None:
    mask = mask & (t <= t_fin)

t_plot = t_shift[mask]
y_plot = datos[mask]

if t_plot.size == 0:
    raise ValueError("El recorte con t_inicio/t_fin dejó 0 muestras. Ajustá parámetros.")

# =========================
# === FUNCIONES DE FILTRO ===
# =========================
def moving_average(x, window_samples):
    if window_samples <= 1:
        return x
    # modo 'same' con padding
    kernel = np.ones(window_samples) / window_samples
    return np.convolve(x, kernel, mode='same')

def median_filter_numpy(x, window_samples):
    # implementación simple (ventana impar)
    if window_samples <= 1:
        return x
    from numpy.lib.stride_tricks import sliding_window_view
    if window_samples > len(x):
        window_samples = len(x) if len(x)%2==1 else len(x)-1
    try:
        sw = sliding_window_view(x, window_samples)
        med = np.median(sw, axis=1)
        # reconstuir con padding en los extremos
        pad = (len(x) - len(med))//2
        return np.concatenate([np.full(pad, med[0]), med, np.full(len(x)-len(med)-pad, med[-1])])
    except Exception:
        # fallback lento
        out = np.copy(x)
        half = window_samples // 2
        for i in range(len(x)):
            a = max(0, i-half)
            b = min(len(x), i+half+1)
            out[i] = np.median(x[a:b])
        return out

def hampel_filter(x, k, t0=3.0):
    # k: ventana en muestras (half-window). t0: n sigma
    n = len(x)
    y = x.copy()
    L = 1.4826  # factor para MAD -> sigma
    for i in range(n):
        a = max(0, i-k)
        b = min(n, i+k+1)
        window = x[a:b]
        med = np.median(window)
        mad = np.median(np.abs(window - med))
        if mad == 0:
            sigma = 0
        else:
            sigma = L * mad
        if sigma == 0:
            continue
        if np.abs(x[i] - med) > t0 * sigma:
            y[i] = med
    return y

# =========================
# === APLICAR FILTRO ===
# =========================
# convertir ms a muestras
def ms_to_samples(ms):
    return max(1, int(round((ms/1000.0) / Ts)))

y_filtered = y_plot.copy()

if method == "median":
    win_samp = ms_to_samples(params["median_window_ms"])
    # asegurar ventana impar
    if win_samp % 2 == 0:
        win_samp += 1
    if SCIPY_AVAILABLE:
        try:
            y_filtered = medfilt(y_plot, kernel_size=win_samp)
        except Exception:
            y_filtered = median_filter_numpy(y_plot, win_samp)
    else:
        y_filtered = median_filter_numpy(y_plot, win_samp)

elif method == "moving_average":
    win_samp = ms_to_samples(params["moving_avg_ms"])
    y_filtered = moving_average(y_plot, win_samp)

elif method == "savitzky_golay":
    if not SCIPY_AVAILABLE:
        raise RuntimeError("savitzky_golay requiere scipy. Instalá scipy o elegí otro método.")
    win_samp = ms_to_samples(params["savgol_window_ms"])
    if win_samp % 2 == 0:
        win_samp += 1
    if win_samp < params["savgol_poly"] + 2:
        win_samp = params["savgol_poly"] + 2
        if win_samp % 2 == 0:
            win_samp += 1
    y_filtered = savgol_filter(y_plot, win_length=win_samp, polyorder=params["savgol_poly"])

elif method == "hampel":
    k = ms_to_samples(params["hampel_window_ms"])
    if k < 1:
        k = 1
    # hampel defined with half-window in our impl
    y_filtered = hampel_filter(y_plot, k, t0=params["hampel_n_sigma"])

elif method == "butterworth":
    if not SCIPY_AVAILABLE:
        raise RuntimeError("butterworth requiere scipy. Instalá scipy o elegí otro método.")
    # cutoff en Hz
    cutoff_hz = params["butter_cutoff_khz"] * 1e3
    nyq = 0.5 * (1.0 / Ts)
    Wn = cutoff_hz / nyq
    if Wn >= 1.0:
        raise ValueError("El cutoff es >= Nyquist. Reducí butter_cutoff_khz o aumentar sampling_rate.")
    b, a = butter(params["butter_order"], Wn, btype='low', analog=False)
    y_filtered = filtfilt(b, a, y_plot)

else:
    raise ValueError(f"Método desconocido: {method}")

# =========================
# === PLOT COMPARATIVO ===
# =========================
plt.figure(figsize=(10,5))
#plt.plot(t_plot * 1e6, y_plot, label="Original", alpha=0.6, linewidth=1)
plt.plot(t_plot * 1e6, 1000*y_filtered, label="Ripple", linewidth=1.5)
plt.xlabel("Tiempo [µs]")
plt.ylabel("Volt [mV]")
#plt.title(f"Despike - método: {method}")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# === OPCIONAL: marcar los valores cambiados (solo para algunos métodos) ===
if method in ("hampel","median") :
    changed_idx = np.where(np.abs(y_plot - y_filtered) > 1e-12)[0]
    if changed_idx.size:
        plt.figure(figsize=(10,3))
        plt.plot(t_plot * 1e6, y_plot, label="Original", alpha=0.5)
        plt.plot(t_plot[changed_idx] * 1e6, y_plot[changed_idx], 'rx', label="Reemplazados")
        plt.xlabel("Tiempo [µs]")
        plt.ylabel("Volt [V]")
        plt.title("Puntos identificados como picos/outliers")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

