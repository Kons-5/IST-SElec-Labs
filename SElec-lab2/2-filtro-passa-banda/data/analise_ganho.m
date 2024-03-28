clear; clc; close all;

%% Read the .csv and unwrap the phase
% Experimental data
exp_data = readtable("filtro-passa-banda-ganho-exp.csv", 'VariableNamingRule', 'preserve');
mag_exp = 20*log10(exp_data{:,2});
phase_exp = exp_data{:,3};

negative_indices = find(phase_exp < 0);                          % Find negative values
phase_exp(negative_indices) = phase_exp(negative_indices) + 360; % and add 360 to them

% Simulation data
sim_data = readtable("filtro-passa-banda-ganho-sim.csv", 'VariableNamingRule', 'preserve');
mag_sim = sim_data{:,2};
phase_sim = unwrap(sim_data{:,3}*pi/180)*180/pi; % avoid phase wrapping

%% Theoric transfer function
R4 = 12 * 10^3; 
R5 = 18 * 10^3;
R6 = 100 * 10^3;
R7 = 560 * 10^3;
C4 = 10 * 10^(-9); 
C5 = 270 * 10^(-12);

num = [-1/((R5+R4) * C5) 0];
den = [1 (C4 + C5)/(R7 * C4 * C5) ((R5+R4) + R6)/((R5+R4) * R6 * R7 * C4 * C5)];

f = logspace(0, 6, 1000); % 1Hz to 100kHz
w = 2 * pi * f;

h = freqs(num, den, w);
mag_teo = mag2db(abs(h)); % convert magnitude to dB
phase_teo = unwrap(phase(h)) * 180/pi + 360; % convert phase to degrees and unwrap

%% Theoric Plot
figure(1);
set(gcf, 'Position',  [100, 100, 660, 340]);
grid on, grid minor;

% change axis tick labels size
ax = gca;
ax.FontSize = 11;
ax.TickLabelInterpreter = 'latex';

% x-axis
xlim([1 1e6])
% set x-axis tick locations and labels
xticks = [1, 10, 100, 1e3, 1e4, 1e5, 1e6];
xticklabels = {'1Hz', '10Hz', '100Hz', '1kHz', '10kHz', '100kHz', '1MHz'};
set(gca, 'XTick', xticks, 'XTickLabel', xticklabels);

yyaxis left;  %%%
p1 = semilogx(f, mag_teo, 'Color', [0 0 0], 'LineWidth', 1.5); hold on
set(gca, 'YColor', [0 0 0])  % change left y-axis color to black
ylim([-10 40]);
set_axis_labels(gca().YAxis(1), 'dB');

% get maximum magnitude, its frequency, and bandwidth
[max_mag, max_freq, max_idx, fL, left_idx, fH, right_idx, bandwidth] = analyze_frequency_response(f, mag_teo);

% plot desired frequencies and magnitudes
xline(fL, '--', 'Color', [0.01 0.24 0.33], 'LineWidth', 1.5);  % left -3dB frequency line
xline(fH, '--', 'Color', [0.01 0.24 0.33], 'LineWidth', 1.5);  % right -3dB frequency line
plot(max_freq, max_mag, 's', 'MarkerSize', 8, 'MarkerFaceColor', [0.93 0.69 0.13], 'MarkerEdgeColor','none');

aux1 = zeros(size(f,2),2);
aux1(:,1) = f; aux1(:,2) = mag_teo;
add_point_annotation(ax, aux1, max_idx, -0.04, -0.015,'kHz', 'dB');
plot(fL, max_mag - 3, '.', 'MarkerSize', 20, 'Color', [0.01 0.24 0.33]);
add_point_annotation(ax, aux1, left_idx, -0.16, -0.03,'Hz', 'dB');
plot(fH, max_mag - 3, '.', 'MarkerSize', 20, 'Color', [0.01 0.24 0.33]);
add_point_annotation(ax, aux1, right_idx, 0.065, -0.029,'kHz', 'dB');

yyaxis right; %%%
p2 = semilogx(f, phase_teo, '--', 'Color', [0.3 0.3 0.3], 'LineWidth', 1.5);
set(gca, 'YColor', [0.1 0.1 0.1])  % change right y-axis color to gray
ylim([90 270]); set(gca, 'YTick', 90:45:270); 
set_axis_labels(gca().YAxis(2), '$^\circ$'); % add degree symbol to y-axis tick labels

legend([p1, p2], 'Magnitude', 'Fase', ...
    'Location', 'best', 'Interpreter', 'latex', 'FontName', 'Times New Roman', 'FontSize', 9);

%% Simulation Plot
figure(2);


%% ExperimentalPlot
figure(3);


%% Functions
% Adds a symbol to the y-axis tick labels
function set_axis_labels(axis, unit)
    axis.Exponent = 0;  % disable scientific notation
    tick_values = get(axis, 'TickValues');
    tick_labels = arrayfun(@(x)[num2str(x), unit], tick_values, 'UniformOutput', false);
    set(axis, 'TickLabels', tick_labels);
end

function [max_mag, max_freq, max_idx, fL, left_idx, fH, right_idx, bandwidth] = analyze_frequency_response(freq, mag)
    % Find max magnitude and its corresponding frequency
    [max_mag, max_idx] = max(mag);
    max_freq = freq(max_idx); % Max magnitude's frequency
    
    % Find the -3dB magnitude
    mag_3dB = max_mag - 3;
    
    % Find closest points to -3dB magnitude on the left and right of the peak
    [~, left_idx] = min(abs(mag(1:max_idx) - mag_3dB));
    [~, right_idx_temp] = min(abs(mag(max_idx:end) - mag_3dB));
    right_idx = right_idx_temp + max_idx - 1;

    fL = freq(left_idx);
    fH = freq(right_idx);

    % Calculate bandwidth
    bandwidth = freq(right_idx) - freq(left_idx);
end

function add_point_annotation(ax, data, idx, offX, offY, x_unit, y_unit)
    % get axes position in normalized units
    axPos = ax.Position;

    % get the axis limits
    ax_xlim = xlim(ax);
    ax_ylim = ylim(ax);

    % convert the data point location to normalized figure coordinates
    if ax.XScale == "log"
        normX = (log10(data(idx,1)) - log10(ax_xlim(1))) / (log10(ax_xlim(2)) - log10(ax_xlim(1)));
    else
        normX = (data(idx,1) - ax_xlim(1)) / (ax_xlim(2) - ax_xlim(1));
    end
    normY = (data(idx,2) - ax_ylim(1)) / (ax_ylim(2) - ax_ylim(1));

    % define text string with frequency and magnitude
    if x_unit == "kHz"
        textStr = sprintf('(%.3f %s, %.3f %s)', data(idx,1)/1000, x_unit, data(idx,2), y_unit);
    else
        textStr = sprintf('(%.3f %s, %.3f %s)', data(idx,1), x_unit, data(idx,2), y_unit);
    end

    % ensure normalized coordinates are within [0, 1]
    normX = min(max(normX, 0), 1);
    normY = min(max(normY, 0), 1);

    % create annotation
    a = annotation('textbox', [axPos(1)+normX*axPos(3)+offX, axPos(2)+normY*axPos(4)+offY, 0.1, 0.1],...
        'String', textStr,...
        'FitBoxToText', 'on',...
        'BackgroundColor', 'none',...
        'EdgeColor', 'none',...
        'FontSize', 10,...
        'HorizontalAlignment', 'center',...
        'VerticalAlignment', 'middle',...
        'Interpreter', 'latex');
end