%% Dados experimentais
y = [322 148 97 85]';         % Amplitudes da tensão vFT (em mV)
x = [8.4 13.1 17.4 19.7]';    % Valores das distâncias (em cm)

%% Modelo da regressão
f1 = fit(x, y, 'power1')

%% Visualização
figure(1);
set(gcf, 'Position',  [100, 100, 660, 400]);

plot(f1); hold on;
plot(x, y, 'x');
grid on; grid minor;

% Customização
ax = gca;
ax.FontSize = 11;
ax.TickLabelInterpreter = 'latex';
set_axis_labels(gca().XAxis(1), 'cm'); % set x-axis tick labels
set_axis_labels(gca().YAxis(1), 'mV'); % set y-axis tick labels

xlabel("Dist\^{a}ncia ao obst\'{a}culo", 'Interpreter', 'latex', 'FontName', 'Times New Roman');
ylabel("Amplitude da tens\~{a}o $v_{FT}$", 'Interpreter', 'latex', 'FontName', 'Times New Roman');

legend('Fitted curve', 'Dados experimentais', 'Interpreter', 'latex', 'Location','best');

%% Funções
function set_axis_labels(axis, unit)
    axis.Exponent = 0;  % disable scientific notation
    tick_values = get(axis, 'TickValues');
    tick_labels = arrayfun(@(x)[num2str(x), unit], tick_values, 'UniformOutput', false);
    set(axis, 'TickLabels', tick_labels);
end