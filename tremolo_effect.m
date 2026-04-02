function tremolo_effect(input, output)
    [input_signal, sample_rate] = audioread(input);
    channels = size(input_signal, 2);
    output_signal = zeros(size(input_signal));
    f_lfo = 10;
    depth = 1;
    time = (0: size(input_signal, 1) - 1)'/sample_rate;
    lfo = 1 + depth * sin(2 * pi * f_lfo * time);
    if channels == 1
        disp("Mono signal");
        output_signal = input_signal .* lfo;
        output_signal = output_signal ./ max(abs(output_signal));
        audiowrite(output, output_signal, sample_rate);
        figure;
        plot(time, input_signal, "red");
        hold on;
        plot(time, output_signal, "green");
        xlabel("Time[s]");
        ylabel("Amplitude");
    else
        disp("Stereo signal");
        output_signal(:, 1) = input_signal(:, 1) .* lfo;
        output_signal(:, 2) = input_signal(:, 2) .* lfo;
        output_signal = output_signal ./ max(max(abs(output_signal)));
        audiowrite(output, output_signal, sample_rate);
        figure;
        subplot(2, 1, 1);
        plot(time, input_signal(:, 1), "red");
        hold on;
        plot(time, output_signal(:, 1), "green");
        title("Left channel");
        xlabel("Time[s]");
        ylabel("Amplitude");
        subplot(2, 1, 2);
        plot(time, input_signal(:, 2), "red");
        hold on;
        plot(time, output_signal(:, 2), "green");
        title("Right channel");
        xlabel("Time[s]");
        ylabel("Amplitude");
    end