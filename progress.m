clc
clear 
close all

% Change video here
video1 = '181-1_re_16s.mkv';
video2 = '181-2_re_16s.mkv';

v = VideoReader(video1);
v_framerate = 30;
v_duration = v.Duration;
v_frame_num = ceil(v_framerate * v_duration);

outputVideo = VideoWriter('Result-1.avi');
outputVideo.FrameRate = v_framerate;
open(outputVideo)

outputVideo_b = VideoWriter('Result_blue-1.avi');
outputVideo_b.FrameRate = v_framerate;
open(outputVideo_b)

frame_num = 0;
light_frame_index = 0;
list_index = 0;
light_frame_num = [];
light_frame_time = [];
frames = [];
frames_rgb = [];
min_max_noise = 255;
mean_noise = [];
list = [];

% get gray value of noises
start_time = v.CurrentTime;
while frame_num < 20
    frame_num = frame_num + 1;
    frame = readFrame(v);
    frame_g = rgb2gray(frame);
    if max(max(frame_g)) < min_max_noise
        min_max_noise = max(max(frame_g));
    end
    mean_noise(frame_num) = mean(frame_g(:));
end
noise_level = mean(mean_noise);
noise_light_value = 130;

frame_num = 0;
v.CurrentTime = start_time;
while hasFrame(v)
%     while v.CurrentTime
    frame_num = frame_num + 1;
    frame = readFrame(v);
    frame_g = rgb2gray(frame);
    [W,L] = size(frame_g);
    max_light = max(max(frame_g));
    [max_light_x, max_light_y] = find(frame_g == max_light);
    
    % for the frame with signals
    if max_light > noise_light_value
        
        % get signal frame number
        light_frame_index = light_frame_index + 1;
        frame_time = frame_num / v_frame_num * v_duration;
        light_frame_time(light_frame_index) = frame_time;
        
        % rough denoise
        for w = 1:W
            for l = 1:L
                if frame_g(w,l) < (max_light-noise_level)
                    frame_g(w,l) = 0;
                end
            end
        end
        
        % final denoise and get signal coordinates
        w = 1;
        l = 1;
        while w <= W
            while w <= W && l <= L
                if frame_g(w,l) ~= 0
                    window = frame_g(max(1,w-2):min(w+2,W),max(1,l-2):min(l+2,L));
                    if mean(window) < frame_g(w,l)/2
                        frame_g(w,l) = 0;
                    else
                        if frame_g(w,l) == max(max(window))
                            list_index = list_index + 1;
                            list(list_index,:) = [frame_time w l];
                            w = w+20;
                            l = l+20;
                        end
                    end
                end
                l = l+1;
            end
            l = 1;
            w = w+1;
        end
    else
        frame_g(:) = 0;
    end
    
    frame_b = frame_g * 0.4;
    frame_rgb = cat(3, frame_b, frame_b, frame_g);
    frames{frame_num} = frame_g;
    frames_rgb{frame_num} = frame_rgb;
end

for write_frame_num = 1:frame_num
    writeVideo(outputVideo,frames{write_frame_num});
    writeVideo(outputVideo_b,frames_rgb{write_frame_num});
end

close(outputVideo)
close(outputVideo_b)

[list_w,~] = size(list);
for i = 1:list_w
    formatSpec = 'Time: %8.4f s  w: %d  l: %d\n';
    fprintf(formatSpec,list(i,:));
end

list_1 = list;
fprintf('List 1 saved.\n\n');

v = VideoReader(video2);
v_framerate = 30;
v_duration = v.Duration;
v_frame_num = ceil(v_framerate * v_duration);

outputVideo = VideoWriter('Result-2.avi');
outputVideo.FrameRate = v_framerate;
open(outputVideo)

outputVideo_b = VideoWriter('Result_blue-2.avi');
outputVideo_b.FrameRate = v_framerate;
open(outputVideo_b)

frame_num = 0;
light_frame_index = 0;
list_index = 0;
light_frame_num = [];
light_frame_time = [];
frames = [];
frames_rgb = [];
min_max_noise = 255;
mean_noise = [];
list = [];

% get gray value of noises
start_time = v.CurrentTime;
while frame_num < 20
    frame_num = frame_num + 1;
    frame = readFrame(v);
    frame_g = rgb2gray(frame);
    if max(max(frame_g)) < min_max_noise
        min_max_noise = max(max(frame_g));
    end
    mean_noise(frame_num) = mean(frame_g(:));
end
noise_level = mean(mean_noise);
noise_light_value = 130;

frame_num = 0;
v.CurrentTime = start_time;
while hasFrame(v)
%     while v.CurrentTime
    frame_num = frame_num + 1;
    frame = readFrame(v);
    frame_g = rgb2gray(frame);
    [W,L] = size(frame_g);
    max_light = max(max(frame_g));
    [max_light_x, max_light_y] = find(frame_g == max_light);
    
    % for the frame with signals
    if max_light > noise_light_value
        
        % get signal frame number
        light_frame_index = light_frame_index + 1;
        frame_time = frame_num / v_frame_num * v_duration;
        light_frame_time(light_frame_index) = frame_time;
        
        % rough denoise
        for w = 1:W
            for l = 1:L
                if frame_g(w,l) < (max_light-noise_level)
                    frame_g(w,l) = 0;
                end
            end
        end
        
        % final denoise and get signal coordinates
        w = 1;
        l = 1;
        while w <= W
            while w <= W && l <= L
                if frame_g(w,l) ~= 0
                    window = frame_g(max(1,w-2):min(w+2,W),max(1,l-2):min(l+2,L));
                    if mean(window) < frame_g(w,l)/2
                        frame_g(w,l) = 0;
                    else
                        if frame_g(w,l) == max(max(window))
                            list_index = list_index + 1;
                            list(list_index,:) = [frame_time w l];
                            w = w+20;
                            l = l+20;
                        end
                    end
                end
                l = l+1;
            end
            l = 1;
            w = w+1;
        end
    else
        frame_g(:) = 0;
    end
    
    frame_b = frame_g * 0.4;
    frame_rgb = cat(3, frame_b, frame_b, frame_g);
    frames{frame_num} = frame_g;
    frames_rgb{frame_num} = frame_rgb;
end

for write_frame_num = 1:frame_num
    writeVideo(outputVideo,frames{write_frame_num});
    writeVideo(outputVideo_b,frames_rgb{write_frame_num});
end

close(outputVideo)
close(outputVideo_b)

[list_w,~] = size(list);
for i = 1:list_w
    formatSpec = 'Time: %8.4f s  w: %d  l: %d\n';
    fprintf(formatSpec,list(i,:));
end

list_2 = list;
fprintf('List 2 saved.\n\n');

% calculate coordinates
list_c = [];
ic = 1;
i2_s = 1;
[list_1_w,~] = size(list_1);
[list_2_w,~] = size(list_2);
for i1 = 1:list_1_w
    for i2 = i2_s:list_2_w
        if list_1(i1,1) == list_2(i2,1)
            list_c(ic,:) = [list_1(i1,:) list_2(i2,2:3) -1 -1 -1];
            ic = ic + 1;
            i2_s = i2;
            break;
        end
    end
end

B = 800;
f = 200;
[list_c_w,~] = size(list_c);
for ic = 1:list_c_w
    Z = B*f/(B+list_c(ic,3)-list_c(ic,5));
    X = B/2-(L/2-list_c(ic,3))/f*(Z-f)-(l/2-list_c(ic,3));
    Y = Z*(mean(list_c(ic,2),list_c(ic,4))-W/2)/f;
    list_c(ic,6:8) = [X Y Z];
end

[list_c_w,~] = size(list_c);
for i = 1:list_c_w
    formatSpec = 'Time: %8.4f s  X: %8.4f  Y: %8.4f  Z: %8.4f\n';
    fprintf(formatSpec,list_c(i,1),list_c(i,6:8));
end