using Plots

# Определение параметров системы
m = 1.0           # Масса тела (кг)
cd = 0.1          # Коэффициент сопротивления воздуха
g = 9.81          # Ускорение свободного падения (м/с²)
v0 = 20.0         # Начальная скорость (м/с)
theta = 45        # Угол запуска (градусы)
dt = 0.01         # Шаг интегрирования
t_max = 5.0       # Максимальное время моделирования

# Преобразование угла в радианы
theta_rad = deg2rad(theta)

# Начальные условия: [x, y, vx, vy]
y0 = [0.0, 0.0, v0 * cos(theta_rad), v0 * sin(theta_rad)]

# Функция для вычисления производных
function equations(y)
    x, y_pos, vx, vy = y
    v = sqrt(vx^2 + vy^2)
    ax = - (cd / m) * vx * v
    ay = -g - (cd / m) * vy * v
    return [vx, vy, ax, ay]
end

# Метод Рунге-Кутты 4-го порядка
function runge_kutta4(f, y0, dt, t_max)
    t = 0.0
    y = y0
    traj = []  # Хранение координат
    while y[2] >= 0  # Пока тело не коснется земли
        push!(traj, (y[1], y[2]))
        k1 = dt * f(y)
        k2 = dt * f(y .+ k1 / 2)
        k3 = dt * f(y .+ k2 / 2)
        k4 = dt * f(y .+ k3)
        y = y .+ (k1 + 2*k2 + 2*k3 + k4) / 6
        t += dt
        if t > t_max  # Прекращаем по времени
            break
        end
    end
    return traj
end

# Запуск численного решения
trajectory = runge_kutta4(equations, y0, dt, t_max)

# Координаты для построения графика
x_vals = [p[1] for p in trajectory]
y_vals = [p[2] for p in trajectory]

# Построение графика
plot(x_vals, y_vals, label="Траектория", xlabel="x (м)", ylabel="y (м)",
 legend=:topright, title="Моделирование полета с сопротивлением воздуха")
scatter!([x_vals[end]], [y_vals[end]], label="Точка падения")
savefig("plot1.png")