% clear; clc; close all;

%% Read the .csv
raw_data1 = readtable("ganhoB-1.csv", 'VariableNamingRule', 'preserve');
raw_data2 = readtable("ganhoB-2.csv", 'VariableNamingRule', 'preserve');

%% Convert dB to linear and to kilo units
linear1 = db2mag(raw_data1{:,2});
linear2 = db2mag(raw_data2{:,2});

%% Unwrap the angle
angle1 = unwrap(raw_data1{:,3}*pi/180)*180/pi; % avoid phase wrapping
angle2 = unwrap(raw_data2{:,3}*pi/180)*180/pi; % avoid phase wrapping

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
xticks = [1, 10, 100, 1e3, 1e4, 1e5 1e6 1e7 1e8];
xticklabels = {'1Hz', '10Hz', '100Hz', '1kHz', '10kHz', '100kHz', '1MHz', '10MHz', '100MHz'};
set(gca, 'XTick', xticks, 'XTickLabel', xticklabels);

% left side
% Encontrar o valor máximo em linear1
maxValue = max(linear1);

% Calcular o valor de -3dB
targetValue = maxValue / sqrt(2);

% Encontrar os índices dos pontos mais próximos de -3dB
% Isso pressupõe que linear1 está em ordem crescente de frequência
leftSide = find(linear1 < targetValue, 1, 'last');
rightSide = find(linear1 < targetValue, 1, 'first');

% Certificar de que encontramos pontos em ambos os lados do pico
if isempty(leftSide) || isempty(rightSide)
    error('Não foi possível encontrar os pontos de -3dB em ambos os lados da banda.');
end

% Plotar os gráficos com pontos marcados
yyaxis left;
semilogx(raw_data1{:,1}, linear1, 'Color', [0 0 1], 'LineWidth', 1.5); hold on;
set(gca, 'YColor', [0 0 0]); % Muda a cor do eixo y esquerdo para preto
ylim([0 100]);

% Marcar os pontos de -3dB
plot(raw_data1{leftSide,1}, linear1(leftSide), 's', 'MarkerSize', 8, ...
    'MarkerFaceColor', [0.93 0.69 0.13], 'MarkerEdgeColor','none');
plot(raw_data1{rightSide,1}, linear1(rightSide), 's', 'MarkerSize', 8, ...
    'MarkerFaceColor', [0.93 0.69 0.13], 'MarkerEdgeColor','none');

% Adicionar anotações se necessário
% Supondo que a função add_point_annotation possa aceitar coordenadas diretamente
add_point_annotation(gca, raw_data1{leftSide,1}, linear1(leftSide), 'kHz', 'V/V');
add_point_annotation(gca, raw_data1{rightSide,1}, linear1(rightSide), 'kHz', 'V/V');

hold off;


%% legend
legend([p1, p2], 'BC547B', 'BC547C', ...
    'Location', 'best', 'Interpreter', 'latex', 'FontName', 'Times New Roman', 'FontSize', 9);

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
    a = annotation('textbox', [axPos(1)+normX*axPos(3)-0.066, axPos(2)+normY*axPos(4)-0.297, 0.1, 0.1],...
        'String', textStr,...
        'FitBoxToText', 'on',...
        'BackgroundColor', 'none',...
        'EdgeColor', 'none',...
        'FontSize', 10,...
        'HorizontalAlignment', 'center',...
        'VerticalAlignment', 'middle',...
        'Interpreter', 'latex');
end