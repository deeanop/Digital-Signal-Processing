function flanger_effect(input, output, max_buffer_size, min_buffer_size, buffer_size)
    [input_signal, sample_rate] = audioread(input);
    channels = size(input_signal, 2);
    if channels == 2
        disp("Stereo signal");
    else
        disp("Mono signal");
    end
    circular_buffer = zeros(buffer_size, channels);
    var = uint32(1);
    output_signal = zeros(size(input_signal));
    modulation_freq = 2;  
    previous_sample_time = (0:length(input_signal)-1)' / sample_rate;
    modulated_delay = min_buffer_size + (max_buffer_size - min_buffer_size)/2 * (1 + sin(2 * pi * modulation_freq * previous_sample_time));
    for i = 1:length(input_signal)
        current_sample = input_signal(i, :);
        divided_input_sample = current_sample * 0.7; %schimbarea valorii de divizare
        current_delay = round(modulated_delay(i));
        position = mod(var - current_delay - 1, buffer_size) + 1;
        delay = circular_buffer(position, :);
        signal_sum = (0.6 * divided_input_sample + 0.4 * delay);  %valori de diverse de divizare 
        circular_buffer(var, :) = signal_sum;
        var = mod(var, buffer_size) + 1;
        output_signal(i, :) = signal_sum .*2; %amplificare finala  
    end
    audiowrite(output, output_signal, sample_rate);

    figure;
    subplot(1, 2, 1);
    if channels == 2
        plot(input_signal(:, 2));
    else
        plot(input_signal);
    end
    xlabel("Number of samples");
    ylabel("Amplitude");
    title("Input signal");
    subplot(1, 2, 2);
    if channels == 2
        plot(output_signal(:, 2));
    else
        plot(output_signal);
    end
    xlabel("Number of samples");
    ylabel("Amplitude");
    title("Output flanger signal");
    xlim([0 1000000]);
    ylim([-1 1]);
end
