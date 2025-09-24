# --- early dispatcher: run submodule directly if requested ---
def _maybe_dispatch_submodule():
    import sys, traceback
    from pathlib import Path

    if "--run-module" in sys.argv:
        # 1) Argümandan modül adını al
        try:
            i = sys.argv.index("--run-module")
            name = sys.argv[i+1]
        except Exception:
            print("Usage: --run-module <MODULE_NAME>")
            sys.exit(2)

        # 2) sys.path'e ilgili paket klasörünü en başa ekle
        #    Böylece alt modül içindeki 'ui_components', 'pdf_processor' gibi "bare import"lar da çalışır.
        try:
            if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
                pkg_dir = Path(sys._MEIPASS) / name
            else:
                pkg_dir = Path(__file__).resolve().parent / name
            if pkg_dir.exists():
                sys.path.insert(0, str(pkg_dir))
        except Exception:
            pass

        # 3) İlgili entrypoint'i çağır
        try:
            if name == "ISKONTO_HESABI":
                from ISKONTO_HESABI.main import main as entry
            elif name == "KARLILIK_ANALIZI":
                from KARLILIK_ANALIZI.gui import main as entry
            elif name == "Musteri_Sayisi_Kontrolu":
                from Musteri_Sayisi_Kontrolu.main import main as entry
            elif name == "YASLANDIRMA":
                from YASLANDIRMA.main import main as entry
            else:
                print(f"[ERROR] Unknown submodule: {name}")
                sys.exit(3)

            entry()          # alt programı çalıştır
        except Exception:
            traceback.print_exc()
            sys.exit(1)
        sys.exit(0)          # alt program bitince süreçten çık

_maybe_dispatch_submodule()
# --- /early dispatcher ---
