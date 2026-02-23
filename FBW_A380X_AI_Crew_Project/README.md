# FBW A380X AI Crew (Gate-to-Gate) – Starter Repo mit Setup-EXE Build

Dieses Paket ist so vorbereitet, dass du es direkt auf GitHub hochladen kannst und **GitHub Actions** daraus ein **Windows-Setup (.exe)** baut.

## Was drin ist

- **Gate-to-Gate State Machine** (Cold & Dark → Shutdown)
- **SOP-YAML Struktur** (realistisch aufgebaut, anpassbar)
- **Doctor/Diagnose** (Community-Ordner, FBW A380X, WASimCommander, Logs)
- **CMD Starter** (Fenster bleibt offen)
- **Inno Setup Script** für `Setup.exe`
- **GitHub Workflow** zum automatischen Build

## Wichtige Hinweise

- Das Projekt ist für **Simulation** gedacht.
- Die SOP-Datei ist eine **strukturierte, realistische Basis**. Die exakten Airline-/Operator-Varianten können abweichen.
- Für **FBW-spezifische Schalter/LVars/H-Events** brauchst du die genaue Zuordnung (siehe `config/lvar_map_template.yaml`).
- Ohne WASimCommander kann das Tool trotzdem starten (Demo/Diagnose), aber nicht alle FBW-spezifischen Aktionen ausführen.

## Schnellstart lokal (ohne EXE)

1. ZIP entpacken
2. `A380X_AI_Install.cmd` doppelklicken
3. `A380X_AI_Doctor.cmd` ausführen
4. `A380X_AI_Run.cmd` ausführen

## GitHub -> automatische Setup.exe

1. Neues Repo erstellen
2. Alle Dateien aus diesem ZIP hochladen
3. In GitHub den Workflow **Build Setup EXE** starten (`Actions` → Workflow auswählen → `Run workflow`)
4. Danach unter dem Workflow-Lauf das **Artifact** herunterladen:
   - `A380X_AI_Setup` (enthält die Setup-EXE)
   - `A380X_AI_Portable` (portable Build)

## Ordner / Pfade

Standard-Arbeitsordner (user-spezifisch):
- `%USERPROFILE%\Documents\FBW_A380_Tools\A380X_AICrew`

## Nächster Schritt für echte FBW-Integration

1. FBW A380X installieren (MSFS 2024 kompatibel)
2. WASimCommander `WASimModule` in den Community-Ordner legen
3. Mit WASimUI die benötigten LVars/H-Events prüfen
4. `config/lvar_map_template.yaml` -> `config/lvar_map.yaml` ausfüllen
5. SOP-Actions auf echte Eventnamen mappen
