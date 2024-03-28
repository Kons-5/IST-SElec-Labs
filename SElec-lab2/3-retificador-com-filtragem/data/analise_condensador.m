clear; clc; close all;

%% Read the .csv and unwrap the phase
% Simulation data
% sim_data = readtable("vo-condensador-sim.csv", 'VariableNamingRule', 'preserve');
% vo_sim = sim_data{:,2};

%% Theoric Plot
figure(1);
set(gcf, 'Position',  [100, 100, 660, 340]);
grid on, grid minor;

C = 100 * 10^(-6);
R = 10 * 10^(3);

t = 0:0.001:15;
vo_teo = 0.38 * (1 - exp(-t./(C * R)));

tau = 1/(R*C);
max_amp = max(vo_teo);

plot(t, vo_teo, "Color", "#D95319", 'LineWidth', 1.5); hold on;
plot([1 1] * tau, [0 1] * 0.63 * max_amp, '--', 'Color', [0.01 0.24 0.33], 'LineWidth', 1.5);
plot([0 1] * tau, [1 1] * 0.63 * max_amp, '--', 'Color', [0.01 0.24 0.33], 'LineWidth', 1.5);
plot(tau, 0.63 * max_amp, '.', 'MarkerSize', 15, 'Color', [0.01 0.24 0.33]);
plot([1 1] * 5 * tau, [0 1] * 0.99 * max_amp, '--', 'Color', [0.01 0.24 0.33], 'LineWidth', 1.5);
plot([0 1] * 5 * tau, [1 1] * 0.99 * max_amp, '--', 'Color', [0.01 0.24 0.33], 'LineWidth', 1.5);
plot(5 * tau, 0.99 * max_amp, '.', 'MarkerSize', 15, 'Color', [0.01 0.24 0.33]);

% Axis
% change axis tick labels size
ax = gca;
ax.FontSize = 11;
ax.TickLabelInterpreter = 'latex';
xlim([0 15]); ylim([0 0.4]);
% set x-axis tick labels
xticks = [0 tau 5*tau]; xticklabels = {'$0\text{s}$', '$\tau$', '5$\tau$'};
set(gca, 'XTick', xticks, 'XTickLabel', xticklabels);
% set y-axis tick labels
yticks = [0 0.63*max_amp 0.99*max_amp]; yticklabels = {'$0\text{V}$', '$0.63\, V_o$', '$0.99\, V_o$'};
set(gca, 'YTick', yticks, 'YTickLabel', yticklabels);

xlabel('Tempo (ms)', 'Interpreter', 'latex', 'FontName', 'Times New Roman');
legend('Esbo\c{c}o de $v_{o}$', 'Interpreter', 'latex', 'Location','best');

%% Simulation Plot
figure(2);
set(gcf, 'Position',  [100, 100, 660, 340]);

plot(t, vo_teo, "Color", "#D95319", 'LineWidth', 1.5); hold on;
plot([1 1] * tau, [0 1] * 0.63 * max_amp, '--', 'Color', [0.01 0.24 0.33], 'LineWidth', 1.5);
plot([0 1] * tau, [1 1] * 0.63 * max_amp, '--', 'Color', [0.01 0.24 0.33], 'LineWidth', 1.5);
plot(tau, 0.63 * max_amp, '.', 'MarkerSize', 15, 'Color', [0.01 0.24 0.33]);
plot([1 1] * 5 * tau, [0 1] * 0.99 * max_amp, '--', 'Color', [0.01 0.24 0.33], 'LineWidth', 1.5);
plot([0 1] * 5 * tau, [1 1] * 0.99 * max_amp, '--', 'Color', [0.01 0.24 0.33], 'LineWidth', 1.5);
plot(5 * tau, 0.99 * max_amp, '.', 'MarkerSize', 15, 'Color', [0.01 0.24 0.33]);

% Axis
% change axis tick labels size
ax = gca;
ax.FontSize = 11;
ax.TickLabelInterpreter = 'latex';
xlim([0 15]); %ylim([0 0.4]);
% set x-axis tick labels
set_axis_labels(gca().XAxis(1), 's');
% set y-axis tick labels
set_axis_labels(gca().YAxis(1), 'V');

legend('Andamento de $v_{o}$', 'Interpreter', 'latex', 'Location','best');
grid on, grid minor;

%% Functions
% Adds a symbol to the y-axis tick labels
function set_axis_labels(axis, unit)
    axis.Exponent = 0;  % disable scientific notation
    tick_values = get(axis, 'TickValues');
    tick_labels = arrayfun(@(x)[num2str(x), unit], tick_values, 'UniformOutput', false);
    set(axis, 'TickLabels', tick_labels);
end