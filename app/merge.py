def merge_transcript_with_speakers(whisper_segments, speaker_segments):
    """
    Whisper ke text segments aur pyannote ke speaker segments ko
    time ke hisaab se match karke ek final structured transcript banata hai.

    2 improvements:
    1. Speaker labels ko "chronological order" mein rename karta hai
       (jo pehle bola usay Speaker 1, jo baad mein bola usay Speaker 2)
    2. Consecutive segments jo same speaker ke hon, unhe ek saath jodta hai
    """

    # Step 1: Har whisper segment ko uska speaker do (raw label ke saath)
    raw_merged = []
    for w_seg in whisper_segments:
        w_start = w_seg["start"]
        w_end = w_seg["end"]
        w_mid = (w_start + w_end) / 2

        matched_speaker = "Unknown"
        for s_seg in speaker_segments:
            if s_seg["start"] <= w_mid <= s_seg["end"]:
                matched_speaker = s_seg["speaker"]
                break

        raw_merged.append({
            "speaker": matched_speaker,
            "start": w_start,
            "end": w_end,
            "text": w_seg["text"].strip()
        })

    # Step 2: Speaker labels ko chronological order mein rename karo
    speaker_order = []
    for seg in raw_merged:
        if seg["speaker"] != "Unknown" and seg["speaker"] not in speaker_order:
            speaker_order.append(seg["speaker"])

    speaker_rename_map = {
        raw_label: f"Speaker {i + 1}"
        for i, raw_label in enumerate(speaker_order)
    }

    for seg in raw_merged:
        if seg["speaker"] in speaker_rename_map:
            seg["speaker"] = speaker_rename_map[seg["speaker"]]

    # Step 3: Consecutive segments jo same speaker ke hain, unhe jodo
    final_merged = []
    for seg in raw_merged:
        if final_merged and final_merged[-1]["speaker"] == seg["speaker"]:
            final_merged[-1]["end"] = seg["end"]
            final_merged[-1]["text"] += " " + seg["text"]
        else:
            final_merged.append({
                "speaker": seg["speaker"],
                "start": round(seg["start"], 2),
                "end": round(seg["end"], 2),
                "text": seg["text"]
            })

    for seg in final_merged:
        seg["start"] = round(seg["start"], 2)
        seg["end"] = round(seg["end"], 2)
        seg["text"] = seg["text"].strip()

    return final_merged