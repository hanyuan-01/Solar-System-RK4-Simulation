import math
import time

print("=" * 50)
print("太阳系轨道模拟 - 龙格-库塔法演示")
print("=" * 50)

# 演示龙格-库塔法原理
def demonstrate_rk4():
    print("\n1. 龙格-库塔法(RK4)原理演示")
    print("-" * 30)
    
    # 简单测试函数: dy/dt = -y
    def test_equation(t, y):
        return -y
    
    # 初始条件
    t0, y0 = 0, 1.0
    dt = 0.5
    exact_solution = y0 * math.exp(-(t0+dt))  # 精确解
    
    # RK4单步计算
    k1 = test_equation(t0, y0)
    k2 = test_equation(t0 + dt/2, y0 + dt/2 * k1)
    k3 = test_equation(t0 + dt/2, y0 + dt/2 * k2)
    k4 = test_equation(t0 + dt, y0 + dt * k3)
    
    y_rk4 = y0 + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)
    
    print(f"测试方程: dy/dt = -y")
    print(f"初始条件: t={t0}, y={y0}")
    print(f"时间步长: dt={dt}")
    print()
    print(f"k1 = f(t, y) = {k1:.6f}")
    print(f"k2 = f(t+dt/2, y+dt/2*k1) = {k2:.6f}")
    print(f"k3 = f(t+dt/2, y+dt/2*k2) = {k3:.6f}")
    print(f"k4 = f(t+dt, y+dt*k3) = {k4:.6f}")
    print()
    print(f"RK4计算结果: y = {y_rk4:.6f}")
    print(f"精确解: y = {exact_solution:.6f}")
    print(f"绝对误差: {abs(y_rk4 - exact_solution):.2e}")

def orbital_equations(t, state, GM):
    """轨道运动方程: state = [x, y, vx, vy]"""
    x, y, vx, vy = state
    r = math.sqrt(x**2 + y**2)
    r3 = r**3
    ax = -GM * x / r3
    ay = -GM * y / r3
    return [vx, vy, ax, ay]  # [dx/dt, dy/dt, dvx/dt, dvy/dt]

def rk4_orbit_step(func, t, state, dt, GM):
    """RK4单步轨道计算"""
    k1 = func(t, state, GM)
    k2_state = [state[i] + dt/2 * k1[i] for i in range(4)]
    k2 = func(t + dt/2, k2_state, GM)
    k3_state = [state[i] + dt/2 * k2[i] for i in range(4)]
    k3 = func(t + dt/2, k3_state, GM)
    k4_state = [state[i] + dt * k3[i] for i in range(4)]
    k4 = func(t + dt, k4_state, GM)
    
    new_state = [state[i] + dt/6 * (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) 
                for i in range(4)]
    return new_state

def calculate_energy(state, GM, mass=1.0):
    """计算轨道机械能"""
    x, y, vx, vy = state
    r = math.sqrt(x**2 + y**2)
    v_sq = vx**2 + vy**2
    kinetic = 0.5 * mass * v_sq
    potential = -GM * mass / r
    return kinetic + potential

# 使用RK4的太阳系模拟
def rk4_solar_simulation():
    print("\n2. RK4太阳系轨道模拟")
    print("-" * 30)
    
    # 物理常数 (标准化单位)
    GM = 4 * math.pi**2  # 对于1AU轨道，周期1年
    
    # 行星初始状态 [x, y, vx, vy]
    planets = {
        "地球": [1.0, 0.0, 0.0, 2 * math.pi],  # 1AU半径，年周期
        "火星": [1.52, 0.0, 0.0, 2 * math.pi / math.sqrt(1.52**3)]  # 开普勒第三定律
    }
    
    dt = 0.01  # 时间步长 (年)
    steps_per_year = int(1.0 / dt)
    
    print("行星初始状态:")
    print("名称\t初始位置(X,Y)\t初始速度(Vx,Vy)")
    print("-" * 45)
    for name, state in planets.items():
        print(f"{name}\t({state[0]:.2f}, {state[1]:.2f})\t({state[2]:.2f}, {state[3]:.2f})")
    
    print("\nRK4轨道演化:")
    print("时间(年)\t地球位置(X,Y)\t地球速度(Vx,Vy)")
    print("-" * 55)
    
    # 存储初始能量用于守恒分析
    initial_energies = {}
    for name, state in planets.items():
        initial_energies[name] = calculate_energy(state, GM)
    
    # 模拟5年的轨道
    for year in range(6):
        # 每年输出一次结果
        earth_state = planets["地球"]
        print(f"{year}\t({earth_state[0]:.3f}, {earth_state[1]:.3f})\t({earth_state[2]:.3f}, {earth_state[3]:.3f})")
        
        # 每年推进steps_per_year步
        for step in range(steps_per_year):
            for name in planets:
                planets[name] = rk4_orbit_step(
                    orbital_equations, 0, planets[name], dt, GM
                )
        
        time.sleep(0.3)

# 基于RK4的真实能量守恒分析
def rk4_stability_analysis():
    print("\n3. RK4轨道稳定性分析")
    print("-" * 30)
    
    GM = 4 * math.pi**2
    earth_state = [1.0, 0.0, 0.0, 2 * math.pi]
    initial_energy = calculate_energy(earth_state, GM)
    
    dt = 0.01
    steps_per_year = int(1.0 / dt)
    
    print("时间(年)\t系统能量\t能量误差\t相对误差")
    print("-" * 50)
    
    for year in range(6):
        # 每年推进steps_per_year步
        for step in range(steps_per_year):
            earth_state = rk4_orbit_step(
                orbital_equations, 0, earth_state, dt, GM
            )
        
        current_energy = calculate_energy(earth_state, GM)
        energy_error = abs(current_energy - initial_energy)
        relative_error = energy_error / abs(initial_energy)
        
        print(f"{year}\t{current_energy:.6f}\t{energy_error:.2e}\t{relative_error:.2e}")
        time.sleep(0.3)

# 基于RK4计算的可视化轨道
def rk4_draw_orbits():
    print("\n4. RK4轨道可视化（字符画）")
    print("-" * 30)
    
    GM = 4 * math.pi**2
    dt = 0.01
    
    # 初始状态
    earth_state = [1.0, 0.0, 0.0, 2 * math.pi]
    mars_state = [1.52, 0.0, 0.0, 2 * math.pi / math.sqrt(1.52**3)]
    
    # 模拟到2.5年
    target_time = 2.5
    total_steps = int(target_time / dt)
    
    for step in range(total_steps):
        earth_state = rk4_orbit_step(orbital_equations, 0, earth_state, dt, GM)
        mars_state = rk4_orbit_step(orbital_equations, 0, mars_state, dt, GM)
    
    # 修正可视化
    size = 21
    center = size // 2
    scale = 6
    
    grid = [[' ' for _ in range(size)] for _ in range(size)]
    
    # 绘制太阳
    grid[center][center] = 'S'
    
    # 绘制轨道圆圈（参考用）
    earth_orbit_radius = 8
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        x = center + int(earth_orbit_radius * math.cos(rad))
        y = center + int(earth_orbit_radius * math.sin(rad))
        if 0 <= x < size and 0 <= y < size:
            grid[y][x] = '.'
    
    mars_orbit_radius = 12
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        x = center + int(mars_orbit_radius * math.cos(rad))
        y = center + int(mars_orbit_radius * math.sin(rad))
        if 0 <= x < size and 0 <= y < size:
            grid[y][x] = '*'
    
    # 修正：基于实际RK4计算结果绘制行星位置
    earth_x, earth_y = earth_state[0], earth_state[1]  # (-1.000, -0.000)
    mars_x, mars_y = mars_state[0], mars_state[1]      # (0.277, -0.766)
    
    # 坐标映射：数学坐标 → 屏幕坐标
    earth_screen_x = center + int(earth_x * scale)
    earth_screen_y = center - int(earth_y * scale)  # 注意：y轴取反
    
    mars_screen_x = center + int(mars_x * scale)
    mars_screen_y = center - int(mars_y * scale)    # 注意：y轴取反
    
    # 在地图位置标记行星
    if 0 <= earth_screen_x < size and 0 <= earth_screen_y < size:
        grid[earth_screen_y][earth_screen_x] = 'E'
    
    if 0 <= mars_screen_x < size and 0 <= mars_screen_y < size:
        grid[mars_screen_y][mars_screen_x] = 'M'
    
    # 打印网格
    print("基于RK4计算的太阳系轨道示意图:")
    print("S = 太阳, E = 地球, M = 火星")
    print("." * size)
    for row in grid:
        print(''.join(row))
    print("." * size)
    
    # 显示计算的位置
    print(f"\nRK4计算的位置 (t={target_time}年):")
    print(f"地球: ({earth_state[0]:.3f}, {earth_state[1]:.3f})")
    print(f"火星: ({mars_state[0]:.3f}, {mars_state[1]:.3f})")

# 对比不同方法的精度
def compare_methods():
    print("\n5. 方法精度对比")
    print("-" * 30)
    
    def euler_step(func, t, state, dt, GM):
        """欧拉方法单步"""
        derivative = func(t, state, GM)
        return [state[i] + dt * derivative[i] for i in range(4)]
    
    GM = 4 * math.pi**2
    initial_state = [1.0, 0.0, 0.0, 2 * math.pi]
    dt = 0.1
    steps = 10  # 模拟1年
    
    # 精确解（圆周运动）
    exact_angle = 2 * math.pi
    exact_x = math.cos(exact_angle)
    exact_y = math.sin(exact_angle)
    
    # RK4模拟
    rk4_state = initial_state.copy()
    for step in range(steps):
        rk4_state = rk4_orbit_step(orbital_equations, 0, rk4_state, dt, GM)
    
    # 欧拉方法模拟
    euler_state = initial_state.copy()
    for step in range(steps):
        euler_state = euler_step(orbital_equations, 0, euler_state, dt, GM)
    
    print("方法\t\t最终位置(X,Y)\t位置误差")
    print("-" * 45)
    print(f"精确解\t\t({exact_x:.3f}, {exact_y:.3f})\t-")
    print(f"RK4方法\t\t({rk4_state[0]:.3f}, {rk4_state[1]:.3f})\t{math.hypot(rk4_state[0]-exact_x, rk4_state[1]-exact_y):.3f}")
    print(f"欧拉方法\t({euler_state[0]:.3f}, {euler_state[1]:.3f})\t{math.hypot(euler_state[0]-exact_x, euler_state[1]-exact_y):.3f}")

# 主程序
def main():
    try:
        # 1. 演示龙格-库塔法原理
        demonstrate_rk4()
        time.sleep(1)
        
        # 2. 使用RK4的太阳系模拟
        rk4_solar_simulation()
        time.sleep(1)
        
        # 3. 基于RK4的稳定性分析
        rk4_stability_analysis()
        time.sleep(1)
        
        # 4. 基于RK4的可视化
        rk4_draw_orbits()
        time.sleep(1)
        
        # 5. 方法精度对比
        compare_methods()
        
        print("\n" + "=" * 50)
        print("RK4太阳系轨道模拟完成!")
        print("=" * 50)
        
        input("\n按回车键退出程序...")
        
    except Exception as e:
        print(f"程序运行出错: {e}")
        import traceback
        traceback.print_exc()
        input("按回车键退出...")

# 运行主程序
if __name__ == "__main__":
    main()
