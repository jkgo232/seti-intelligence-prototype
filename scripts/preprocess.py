from blimpy import Waterfall 
import matplotlib.pyplot as plt
import numpy as np

# ------------------------------- Configuration -------------------------------
DATA_PATH = "Hip66704_0005.h5" 

OUTPUT_PATH_rspec = "figures/raw_spectrum.png"
OUTPUT_PATH_rwf = "figures/raw_waterfall.png"
OUTPUT_PATH_spec = "figures/processed_spectrum.png"
OUTPUT_PATH_wf = "figures/processed_waterfall.png"

# Conservative, well-known RFI bands (MHz)
RFI_BANDS_MHZ = [ (1170, 1180), # GPS L5 
(1210, 1230), # GPS L2 
(1570, 1580), # GPS L1 
(1610, 1630), # Iridium 
]
# ------------------------------- Load data -------------------------------
wf = Waterfall(DATA_PATH) 
spec = wf.data.squeeze() # (time, frequency) 
freqs_mhz = wf.get_freqs() 
times = np.arange(spec.shape[0]) * wf.header["tsamp"]
print(len(spec[0]), len(spec[1]), len(freqs_mhz))

# ------------------------------- Plot Raw Data-------------------------------
raw_spectrum = np.median(spec, axis=0)
plt.figure(figsize=(10, 4))
plt.plot(freqs_mhz, raw_spectrum, linewidth=0.8)
plt.xlabel("Frequency (MHz)")
plt.ylabel("Power (arbitrary units)")
plt.title("Raw Spectrum")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_PATH_rspec, dpi=150)
plt.close()
print(f"Saved raw spectrum to {OUTPUT_PATH_rspec}")

plt.figure(figsize=(10, 6))
im = plt.imshow(
    spec,
    aspect="auto",
    origin="lower",
    interpolation="nearest",
    extent=[
        freqs_mhz[0],
        freqs_mhz[-1],
        times[0],
        times[-1],
    ],
    cmap="viridis",
)
plt.xlabel("Frequency (MHz)")
plt.ylabel("Time (s)")
plt.title("Raw Waterfall")
cbar = plt.colorbar(im)
cbar.set_label("Power (arbitrary units)")
plt.tight_layout()
plt.savefig(OUTPUT_PATH_rwf, dpi=150)
plt.close()
print(f"Saved raw waterfall to {OUTPUT_PATH_rwf}")

# ------------------------------- Preprocessing ------------------------------- Remove per-channel baseline
spec -= np.median(spec, axis=0)
# Normalize
spec /= np.std(spec)
# Mask known RFI bands
for fmin, fmax in RFI_BANDS_MHZ: 
  mask = (freqs_mhz >= fmin) & (freqs_mhz <= fmax) 
  spec[:, mask] = np.nan # use NaN so it disappears in plots

# ------------------------------- Compute spectrum ------------------------------- Time-averaged spectrum (ignores NaNs)
spectrum = np.nanmean(spec, axis=0)

# ------------------------------- Plot -------------------------------
plt.figure(figsize=(10, 4)) 
plt.plot(freqs_mhz, spectrum, linewidth=0.8) 
plt.xlabel("Frequency (MHz)") 
plt.ylabel("Normalized Power (σ units)") 
plt.title("Time-Averaged Spectrum After Preprocessing") 
plt.grid(alpha=0.3) 
for fmin, fmax in RFI_BANDS_MHZ: 
    plt.axvspan(fmin, fmax, color="red", alpha=0.1)
plt.tight_layout() 
plt.savefig(OUTPUT_PATH_spec, dpi=150) 
plt.close() 
print(f"Saved processed spectrum to {OUTPUT_PATH_spec}")


plt.figure(figsize=(10, 6))
im = plt.imshow(
    spec,
    aspect="auto",
    origin="lower",
    interpolation="nearest",
    extent=[
        freqs_mhz[0],
        freqs_mhz[-1],
        times[0],
        times[-1],
    ],
    vmin=-3,
    vmax=3,
    cmap="viridis",
)
plt.xlabel("Frequency (MHz)")
plt.ylabel("Time (s)")
plt.title("Processed Waterfall (Baseline-Subtracted, Normalized)")
cbar = plt.colorbar(im)
cbar.set_label("Normalized Power (σ units)")
plt.tight_layout()
plt.savefig(OUTPUT_PATH_wf, dpi=150)
plt.close()
print(f"Saved processed waterfall to {OUTPUT_PATH_wf}")
