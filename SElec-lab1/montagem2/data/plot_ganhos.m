clear; clc; close all;

%% Read the .csv
raw_data1 = readtable("ganho-B.csv", 'VariableNamingRule', 'preserve');
raw_data2 = readtable("ganho-C.csv", 'VariableNamingRule', 'preserve');

%% Convert dB to linear and to kilo units
linear1 = db2mag(raw_data1{:,2});
linear2 = db2mag(raw_data2{:,2});

%% Unwrap the phase
phase1 = unwrap(raw_data1{:,3}*pi/180)*180/pi; % avoid phase wrapping
phase2 = unwrap(raw_data2{:,3}*pi/180)*180/pi; % avoid phase wrapping

%% Plot
figure
set(gcf, 'Position',  [100, 100, 660, 340]);
grid on, grid minor;

% change axis tick labels size
ax = gca;
ax.FontSize = 11;
ax.TickLabelInterpreter = 'latex';

% x-axis
xlim([1 1e6])
% set x-axis tick locations and labels
xticks = [1, 10, 100, 1e3, 1e4, 1e5 1e6];
xticklabels = {'1Hz', '10Hz', '100Hz', '1kHz', '10kHz', '100kHz', '1MHz'};
set(gca, 'XTick', xticks, 'XTickLabel', xticklabels);

% left side
yyaxis left; 
p1 = semilogx(raw_data1{:,1}, linear1, 'Color', [1 0 0], 'LineWidth', 1.5); hold on;
p2 = semilogx(raw_data2{:,1}, linear2, 'Color', [1 0 1], 'LineWidth', 1.5); hold on;
% ylim([0 30]);
set(gca, 'YColor', [0 0 0])  % change left y-axis color to black
% set_axis_labels(gca().YAxis(1), ''); % add kilo-ohm symbol to y-axis tick labels
% find closest frequency to 1 kHz
[~, idx] = min(abs(raw_data1{:,1} - 1000));
plot(raw_data1{idx,1}, linear1(idx), 's', 'MarkerSize', 8, ...
    'MarkerFaceColor', [0.93 0.69 0.13], 'MarkerEdgeColor','none'); hold on;
add_point_annotation(ax, raw_data1, idx, 'kHz', 'V/V');

[~, idx] = min(abs(raw_data2{:,1} - 1000));
plot(raw_data2{idx,1}, linear2(idx), 's', 'MarkerSize', 8, ...
    'MarkerFaceColor', [0.93 0.69 0.13], 'MarkerEdgeColor','none'); hold off;
add_point_annotation(ax, raw_data2, idx, 'kHz', 'V/V');

% right side
yyaxis right; 
semilogx(raw_data1{:,1}, phase1, '--', 'Color', [1 0 0], 'LineWidth', 1.5); hold on;
semilogx(raw_data2{:,1}, phase2, '--', 'Color', [1 0 1], 'LineWidth', 1.5);
set(gca, 'YColor', [0.1 0.1 0.1])  % change right y-axis color to gray
set_axis_labels(gca().YAxis(2), '$^\circ$'); % add degree symbol to y-axis tick labels

%% Legends
legend([p1, p2], {'BC547B', 'BC547C'}, 'Location', 'best', 'Interpreter', 'latex', 'FontName', 'Times New Roman', 'FontSize', 9);

%% Functions
% Adds a symbol to the y-axis tick labels
function set_axis_labels(axis, unit)
    axis.Exponent = 0;  % disable scientific notation
    tick_values = get(axis, 'TickValues');
    tick_labels = arrayfun(@(x)[num2str(x), unit], tick_values, 'UniformOutput', false);
    set(axis, 'TickLabels', tick_labels);
end

function add_point_annotation(ax, data, idx, x_unit, y_unit)
    % convert the table to array
    dataArray = table2array(data);

    % get axes position in normalized units
    axPos = ax.Position;

    % get the axis limits
    ax_xlim = xlim(ax);
    ax_ylim = ylim(ax);

    % convert the data point location to normalized figure coordinates
    if ax.XScale == "log"
        normX = (log10(dataArray(idx,1)) - log10(ax_xlim(1))) / (log10(ax_xlim(2)) - log10(ax_xlim(1)));
    else
        normX = (dataArray(idx,1) - ax_xlim(1)) / (ax_xlim(2) - ax_xlim(1));
    end
    normY = (dataArray(idx,2) - ax_ylim(1)) / (ax_ylim(2) - ax_ylim(1));

    % define text string with frequency and magnitude
    textStr = sprintf('(%.1f %s, %.1f %s)', dataArray(idx,1)/1000, x_unit, db2mag(dataArray(idx,2)), y_unit);

    % ensure normalized coordinates are within [0, 1]
    normX = min(max(normX, 0), 1);
    normY = min(max(normY, 0), 1);

    % create annotation
    a = annotation('textbox', [axPos(1)+normX*axPos(3), axPos(2)+normY*axPos(4), 0.1, 0.1],...
        'String', textStr,...
        'FitBoxToText', 'on',...
        'BackgroundColor', 'none',...
        'EdgeColor', 'none',...
        'FontSize', 10,...
        'HorizontalAlignment', 'center',...
        'VerticalAlignment', 'middle',...
        'Interpreter', 'latex');
end