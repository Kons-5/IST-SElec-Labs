%% Dados experimentais
y = [-10 -5 0 5 10]';
x = [1168.94 1581.62 1992.93 2411.76 2828.69]';

%% Modelo da regressão
f1 = fitlm(x, y, 'linear')

%% Visualização
figure(1);
set(gcf, 'Position',  [100, 100, 660, 400]);

plot(f1); hold on;
plot(x, y, 'o');
grid on; grid minor;

% Customização
ax = gca;
ax.FontSize = 11;
ax.TickLabelInterpreter = 'latex';
set_axis_labels(gca().XAxis(1), ''); % set x-axis tick labels
set_axis_labels(gca().YAxis(1), 'V'); % set y-axis tick labels

xlabel("N\'{i}vel digital ($0$ a $4095$)", 'Interpreter', 'latex', 'FontName', 'Times New Roman');
ylabel("Amplitude da tens\~{a}o de entrada", 'Interpreter', 'latex', 'FontName', 'Times New Roman');

legend('Fitted curve', 'Dados experimentais', 'Interpreter', 'latex', 'Location','best');

%% Funções
function set_axis_labels(axis, unit)
    axis.Exponent = 0;  % disable scientific notation
    tick_values = get(axis, 'TickValues');
    tick_labels = arrayfun(@(x)[num2str(x), unit], tick_values, 'UniformOutput', false);
    set(axis, 'TickLabels', tick_labels);
end