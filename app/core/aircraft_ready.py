
import time

def wait_for_ready(get_snapshot, log, timeout_s: int = 180) -> bool:
    """
    Ready-Check: wartet, bis das Aircraft geladen ist und Basisdaten stabil sind.
    """
    start = time.time()
    last_title = None
    stable_hits = 0

    log(f"[READY] Warte auf Aircraft-Ready (Timeout {timeout_s}s) ...")

    while time.time() - start < timeout_s:
        snap = get_snapshot()

        title = (snap.get("title") or "")
        title_l = title.lower()
        pos_ok = bool(snap.get("position_ok"))
        src = snap.get("source", "unknown")

        # A380-Heuristik
        a380_ok = ("a380" in title_l) or ("a380x" in title_l)

        # Stabilitäts-Check: gleiche Title + Position ok mehrere Zyklen
        if title and pos_ok and a380_ok:
            if title == last_title:
                stable_hits += 1
            else:
                stable_hits = 1
                last_title = title
        else:
            stable_hits = 0
            last_title = title

        log(f"[READY] src={src} title='{title}' a380={a380_ok} pos={pos_ok} stable={stable_hits}/3")

        if stable_hits >= 3:
            log("[READY] OK: Aircraft bereit und stabil.")
            return True

        time.sleep(2.0)

    log("[READY] Timeout: Aircraft nicht bereit geworden.")
    return False
