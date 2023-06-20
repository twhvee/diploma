def get_saving_frames_durations(cap, saving_fps):
    s = []
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s
def getframe(video_file, dirname):  
    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)
    count = 0
    save_count = 0
    while True:
         is_read, frame = cap.read()
         if not is_read:
             break
         frame_duration = count / fps
         try:
             closest_duration = saving_frames_durations[0]
         except IndexError:
             break
         if frame_duration >= closest_duration:
             frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
             saveframe_name = os.path.join(dirname, f"frame{frame_duration_formatted}.jpg")
             cv2.imwrite(saveframe_name, frame)
             save_count += 1
             print(f"{saveframe_name} сохранён")
             try:
                 saving_frames_durations.pop(0)
             except IndexError:
                 pass
         count += 1
         
    print(f"Итого сохранено кадров {save_count}")
     
