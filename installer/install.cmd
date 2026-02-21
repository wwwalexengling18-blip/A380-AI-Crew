FBW_A380X_AI_Crew/
  README.md
  LICENSE
  CHANGELOG.md

  /release/
    build_release.ps1        (packt ZIP)
    build_release.cmd        (startet build, /k)

  /installer/
    install.cmd              (User startet das)
    run.cmd                  (User startet das)
    uninstall.cmd            (optional, sauber entfernen)
    config.example.yaml

  /src/
    ai_crew/
      main.py
      simconnect_bridge.py
      state_machine.py
      checklist_engine.py
      gsx_adapter.py
      hotas_adapter.py
      logger.py

  /assets/
    checklists/
      a380x_gate_to_gate.yaml
    profiles/
      tflight_hotas_x.yaml

  /deps/
    (leer im repo – wird per installer geladen oder per Release mitgeliefert)

  /logs/
    (wird zur Laufzeit erzeugt, nicht committen)

  .gitignore
