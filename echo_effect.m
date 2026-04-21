function echo_effect(input, output, max_buffer_size, min_buffer_size, buffer_size)
    [input_signal, sample_rate] = audioread(input);

    chanels = size(input_signal, 2);
    circular_buffer = zeros(buffer_size, chanels);
    var = uint32(1);
    output_signal = zeros(size(input_signal));
    modulation_freq = 0.5
    t = (0:length(input_signal)-1)'/sample_rate;
    modulated_delay = min_buffer_size + (max_buffer_size - min_buffer_size)/2 * (1 + sin(2 * pi * modulation_freq * t));
    
    for i = 1:length(input_signal)
        sample_current = input_signal(i, :);
        divided_sample = sample_current /2;
        D = round(modulated_delay(i));
        position = mod(var -D -1, buffer_size) + 1;
        delay = circular_buffer(position, :);
        signal_sum = (divided_sample + delay) /2;
        circular_buffer(var, :) = signal_sum;
        var = mod(var, buffer_size) + 1;
        output_signal(i, :) = signal_sum;
    end
    
    audiowrite(output, output_signal, sample_rate);

    figure;
    subplot(1, 2, 1);
    plot(input_signal);
    xlabel("Sample number");
    ylabel("Amplitude");
    title("Input signal");
    subplot(1, 2, 2);
    xlabel("Sample number");
    ylabel("Amplitude");
    title("Output flanger signal");
    
