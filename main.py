import os
import ffmpeg


def compress_video(video_full_path, output_file_name, target_size):
    min_audio_bitrate = 32000
    max_audio_bitrate = 256000

    probe = ffmpeg.probe(video_full_path)

    # Video duration, in s.
    duration = float(probe['format']['duration'])

    # Audio bitrate, in bps.
    audio_bitrate = float(next(
        (s for s in probe['streams'] if s['codec_type'] == 'audio'), None)
        ['bit_rate'])

    # Target total bitrate, in bps.
    target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

    # Target audio bitrate, in bps.
    if 10 * audio_bitrate > target_total_bitrate:
        audio_bitrate = target_total_bitrate / 10
        if audio_bitrate < min_audio_bitrate < target_total_bitrate:
            audio_bitrate = min_audio_bitrate
        elif audio_bitrate > max_audio_bitrate:
            audio_bitrate = max_audio_bitrate

    # Target video bitrate, in bps.
    video_bitrate = target_total_bitrate - audio_bitrate

    i = ffmpeg.input(video_full_path)
    ffmpeg.output(
        i, os.devnull, **{
            'c:v': 'libx264',
            'b:v': video_bitrate,
            'pass': 1,
            'f': 'mp4'
        }).overwrite_output().run()
    ffmpeg.output(
        i, output_file_name, **{
            'c:v': 'libx264',
            'b:v': video_bitrate,
            'pass': 2,
            'c:a': 'aac',
            'b:a': audio_bitrate
        }).overwrite_output().run()


if __name__ == '__main__':
    # Compress input.mp4 to 5MB and save as output.mp4
    compress_video('input.mp4', 'output.mp4', 5 * 1000)
