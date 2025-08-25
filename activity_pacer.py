import os
import sys
from gtts import gTTS
from pydub import AudioSegment
from pydub.generators import Sine

# example create an audio file that has 10 reps where each rep has three activities the first taking 5 seconds the second taking 10 and the last taking 5 seconds.
# python activity_pacer.py 10 5,10,5

def create_custom_audio_file(max_count, silence_durations):
    """
    Generates an MP3 file that counts from 1 to a specified number,
    with customizable periods of silence and beeps in between the 
    periods of silence except for the last period when the next 
    number plays.

    Args:
        max_count (int): The highest number to count to.
        silence_durations (list[int]): A list of integers representing seconds of silence.
    """
    print("🚀 Starting the audio creation process...")

    # 1. Generate the beep sounds internally
    print("   - Generating beep tones...")
    # Standard beep for in-between counts
    beep = Sine(1000).to_audio_segment(duration=200, volume=-20)
    # Final beep for the very end of the file
    final_beep = Sine(200).to_audio_segment(duration=200, volume=-20)

    # 2. Initialize an empty audio segment for the final output
    final_audio = AudioSegment.empty()
    temp_filename = "temp_number.mp3"

    # 3. Loop from 1 to max_count to build the audio track
    for i in range(1, max_count + 1):
        print(f"   - Processing number: {i}")

        # Generate the spoken number using Google Text-to-Speech
        try:
            tts = gTTS(text=str(i), lang='en')
            tts.save(temp_filename)
        except Exception as e:
            print(f"Error generating speech for number {i}: {e}")
            print("Please check your internet connection.")
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
            return

        # Load the spoken number audio
        number_audio = AudioSegment.from_mp3(temp_filename)

        # Add the spoken number to our final audio
        final_audio += number_audio

        # Add the periods of silence and beeps
        num_silences = len(silence_durations)
        for j, seconds in enumerate(silence_durations):
            print(f"     - Adding {seconds} second pause...")
            # Create silent pause, converting seconds to milliseconds
            pause = AudioSegment.silent(duration=seconds * 1000)
            final_audio += pause

            # Add a beep after the pause, except for the last one
            if j < num_silences - 1:
                print("       - Adding beep.")
                final_audio += beep

    # 4. Clean up the temporary number file
    if os.path.exists(temp_filename):
        os.remove(temp_filename)

    # 5. Add the final, lower-frequency beep at the end of the entire sequence
    print("   - Adding final beep...")
    final_audio += final_beep

    # 6. Define output directory and create if it doesn't exist
    output_dir = "output"
    if not os.path.exists(output_dir):
        print(f"   - Creating directory: '{output_dir}'")
        os.makedirs(output_dir)

    # 7. Format the output filename to be inside the output directory
    silence_str = "-".join(map(str, silence_durations))
    base_filename = f"{max_count}_reps-{silence_str}.mp3"
    output_filename = os.path.join(output_dir, base_filename)

    # 8. Export the final combined audio to an MP3 file
    print(f"\n✅ Exporting the final audio to '{output_filename}'...")
    try:
        final_audio.export(output_filename, format="mp3")
        print("🎉 All done! Your file is ready.")
    except Exception as e:
        print(f"Error exporting the final audio file: {e}")


if __name__ == "__main__":
    # Check for the correct number of command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python activity_pacer.py <max_count> <silence_durations>")
        print("Example: python activity_pacer.py 10 5,10,5")
        sys.exit(1)
    try:
        # Parse the first argument (max count)
        count = int(sys.argv[1])

        # Parse the second argument (comma-separated seconds of silence)
        silences = [int(item) for item in sys.argv[2].split(',')]

        # Run the main function with the parsed arguments
        create_custom_audio_file(count, silences)

    except ValueError:
        print("Error: Invalid input.")
        print("Please ensure <max_count> is an integer and <silence_durations> is a comma-separated list of integers.")
        sys.exit(1)
