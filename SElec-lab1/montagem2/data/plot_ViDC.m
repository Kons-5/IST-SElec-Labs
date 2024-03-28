clear; clc; close all;

%% Read the .csv
raw_data1 = readtable("vCE-B.csv", 'VariableNamingRule', 'preserve');
raw_data2 = readtable("vCE-C.csv", 'VariableNamingRule', 'preserve');

%% Convert assign Vi and Vo
vi1 = raw_data1{:,1};
vi2 = raw_data2{:,1};
vo1 = raw_data1{:,2};
vo2 = raw_data2{:,2};

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

%%
set_axis_labels(gca().XAxis(1), 'V'); % add volt symbol to y-axis tick labels

%%

% left side
p1 = plot(vi1, vo1, 'Color', [1 0 0], 'LineWidth', 1.5); hold on;
p2 = plot(vi2, vo2, 'Color', [1 0 1], 'LineWidth', 1.5); hold on;
set(gca, 'YColor', [0 0 0])  % change left y-axis color to black
set_axis_labels(gca().YAxis(1), 'V'); % add volt symbol to y-axis tick labels

%find closest value to previous V_CE
[~, idx] = min(abs(vo1 - 2.466));
plot(vi1(idx), vo1(idx), 's', 'MarkerSize', 8, ...
    'MarkerFaceColor', [0.93 0.69 0.13], 'MarkerEdgeColor','none'); hold on;
add_point_annotation(ax, raw_data1, idx, 'V', 'V');
yline(vo1(idx), '--', 'Linewidth', 1.5);

[~, idx] = min(abs(vo2 - 1.847));
plot(vi1(idx), vo2(idx), 's', 'MarkerSize', 8, ...
    'MarkerFaceColor', [0.93 0.69 0.13], 'MarkerEdgeColor','none'); hold off;
add_point_annotation(ax, raw_data2, idx, 'V', 'V');
yline(vo2(idx), '--', 'Linewidth', 1.5);


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
    textStr = sprintf('(%.3f %s, %.3f %s)', dataArray(idx,1), x_unit, dataArray(idx,2), y_unit);

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