import math

# Speed of sound in different materials
speed_of_sound_materials = {
    "reed": 330,  # Approximate speed of sound in reed (m/s)
    "pvc": 343    # Speed of sound in air (PVC pipes resonate with air column)
}

# Frequency of notes based on key categories

base_frequencies = {
    "low": {
        "C": 130.81, "C#": 138.59, "D": 146.83, "D#": 155.56, "E": 164.81,
        "F": 174.61, "F#": 185.00, "G": 196.00, "G#": 207.65, "A": 220.00,
        "A#": 233.08, "B": 246.94
    },
    "middle": {
        "C": 261.63, "C#": 277.18, "D": 293.66, "D#": 311.13, "E": 329.63,
        "F": 349.23, "F#": 369.99, "G": 392.00, "G#": 415.30, "A": 440.00,
        "A#": 466.16, "B": 493.88
    },
    "high": {
        "C": 523.25, "C#": 554.37, "D": 587.33, "D#": 622.25, "E": 659.25,
        "F": 698.46, "F#": 739.99, "G": 783.99, "G#": 830.61, "A": 880.00,
        "A#": 932.33, "B": 987.77
    }
}

# Updated Ethiopian scales based on keyboard reference (Left to Right order)

scales = {
    "1": {"Major": [1, 1, 0.5, 1, 1, 1, 0.5], "Minor": [1, 0.5, 1, 1, 0.5, 1, 1], "Pentatonic": [1, 1, 1.5, 1, 1.5]},
    "2": {"Maqam Rast": [1, 1, 0.5, 1, 1, 1, 0.5], "Maqam Hijaz": [0.5, 1.5, 0.5, 1, 0.5, 1.5, 0.5]},
    "3": {"Blues": [1.5, 1, 0.5, 0.5, 1.5, 1]},
    "4": {
        "Tizita": [1, 1, 1.5, 1],  # Updated interval,
        "Bati": [2, 0.5 ,1 ,2],  # Updated interval,
        "Anchihoye": [0.5, 2, 0.5 ,2],  # Updated interval,
        "Ambassel": [0.5, 2, 1, 0.5]  # Updated interval
    }
}

def get_scale_notes(scale_intervals, key, note_range):
    notes_order = list(base_frequencies[note_range].keys())
    if key not in notes_order:
        return ["Unknown"]
    
    start_index = notes_order.index(key)
    scale_notes = [key]
    current_index = start_index
    
    for interval in scale_intervals:
        step = round(interval * 2)
        current_index += step
        if current_index >= len(notes_order):
            current_index -= len(notes_order)
        scale_notes.append(notes_order[current_index])
    
    return scale_notes

def get_flute_details(flute_material, scale_category, scale_type, key, diameter, note_range):
    
    if scale_category not in scales or scale_type not in scales[scale_category] or key not in base_frequencies[note_range]:
        return "Invalid selection. Please choose a valid scale category, scale type, and key."
    
    speed_of_sound = speed_of_sound_materials[flute_material]  # Select speed of sound based on material
    key_frequency = base_frequencies[note_range][key]
    intervals = scales[scale_category][scale_type]
    radius = (diameter / 2) / 10
    
    if scale_category == "4":
        intervals = intervals[:4]
    
    fundamental_length = speed_of_sound / (2 * key_frequency)
    corrected_length = fundamental_length + (0.6 * radius)
    
    scale_notes = get_scale_notes(intervals, key, note_range)
    
    hole_positions = []
    total_interval = sum(intervals)
    
    for idx, step in reversed(list(enumerate(intervals, 1))):
        frequency = key_frequency * (2 ** (sum(intervals[:idx]) / 12))
        hole_position = max(0.1, corrected_length - ((sum(intervals[:idx]) / total_interval) * corrected_length))
        hole_diameter = diameter * 0.5
        note_letter = scale_notes[idx]
        adjusted_position = round(hole_position * 100, 2)
        hole_positions.append((idx, adjusted_position, round(hole_diameter, 2), round(frequency, 2), note_letter))
    
    
    
    return {
        "Flute Length (cm, Hz, Note)": (round(corrected_length * 100, 2), round(key_frequency, 2), key),
        "Hole Positions": hole_positions,
        "Scale Notes": scale_notes,
        "Scale Intervals": intervals,
        "Number of Holes": len(hole_positions),
        "Total Notes": len(intervals) + 1
    }

def main():
    
    print("Flute Maker Calculator\n")
    flute_material = input("Select flute material (reed/pvc): ").strip().lower()
    if flute_material not in speed_of_sound_materials:
        print("Invalid material selection. Defaulting to pvc.")
        flute_material = "pvc"
    
    scale_category = input("Enter scale category (1-Western, 2-Arab, 3-R&B, 4-Ethiopian): \n")
    print("\nAvailable scale types:")
    
    for num, name in enumerate(scales[scale_category].keys(), 1):
        print(f"{num}. {name}")
    
    scale_type = input("\nEnter the number of the scale type: ")
    scale_type = list(scales[scale_category].keys())[int(scale_type) - 1]
    
    print("\nChoose the flute range:")
    print("1. Low\n2. Middle\n3. High\n")
    note_range = {"1": "low", "2": "middle", "3": "high"}.get(input("Enter the number: \n"), "middle")
    
    key = input("\nEnter the key (C, C#, D, etc.): \n")
    diameter = float(input("\nEnter the flute's diameter in mm: \n"))
    
    print("\nCalculating flute details...\n")
    print(f"Selected Material: {flute_material}, Key: {key}, Scale Type: {scale_type}, Diameter: {diameter} mm\n")
    result = get_flute_details(flute_material, scale_category, scale_type, key, diameter, note_range)
    
    if isinstance(result, str):
        print(result)
        return
    
    print(f"\nScale Notes: {' - '.join(result['Scale Notes'])}\n")
    flute_length_info = result['Flute Length (cm, Hz, Note)']
    print(f"\nFlute Length: {flute_length_info[0]} cm, Frequency: {flute_length_info[1]} Hz, Note: {flute_length_info[2]}\n")
    print("Hole Positions:\n")
    
    for idx, pos, d, freq, note in result["Hole Positions"]:
        print(f"Hole {idx}: {pos} cm from bottom, Diameter: {d} mm, Frequency: {freq} Hz, Note: {note}\n")

if __name__ == "__main__":
    main()
