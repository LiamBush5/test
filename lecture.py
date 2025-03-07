class Ball:
    def __init__(self, radius=10, center_x=0, center_y=0, color="White"):
        self.radius = radius
        self.center_x = center_x
        self.center_y = center_y
        # Physics properties
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration_x = 0
        self.acceleration_y = 0
        self.mass = radius * 0.1  # Mass proportional to radius
        self.elasticity = 0.8  # Bounce factor (1 = perfect bounce, 0 = no bounce)
        self.color = color

    def __str__(self) -> str:
        return f'radius: {self.radius}, center_x: {self.center_x}, center_y: {self.center_y}, color: {self.color}'

    def apply_force(self, force_x, force_y):
        """Apply a force to the ball, changing its acceleration."""
        self.acceleration_x += force_x / self.mass
        self.acceleration_y += force_y / self.mass

    def apply_gravity(self, gravity=9.8):
        """Apply gravity force."""
        self.acceleration_y += gravity

    def update_position(self, time_step=0.1):
        """Update velocity and position based on acceleration and current velocity."""
        # Update velocity based on acceleration
        self.velocity_x += self.acceleration_x * time_step
        self.velocity_y += self.acceleration_y * time_step

        # Update position based on velocity
        self.center_x += self.velocity_x * time_step
        self.center_y += self.velocity_y * time_step

        # Reset acceleration (forces need to be applied each frame)
        self.acceleration_x = 0
        self.acceleration_y = 0

    def check_boundary_collision(self, width, height):
        """Check for collisions with boundaries and bounce."""
        # Floor collision (bottom boundary)
        if self.center_y + self.radius > height:
            self.center_y = height - self.radius
            self.velocity_y = -self.velocity_y * self.elasticity

        # Ceiling collision (top boundary)
        if self.center_y - self.radius < 0:
            self.center_y = self.radius
            self.velocity_y = -self.velocity_y * self.elasticity

        # Right wall collision
        if self.center_x + self.radius > width:
            self.center_x = width - self.radius
            self.velocity_x = -self.velocity_x * self.elasticity

        # Left wall collision
        if self.center_x - self.radius < 0:
            self.center_x = self.radius
            self.velocity_x = -self.velocity_x * self.elasticity

    def check_ball_collision(self, other_ball):
        """Check for collision with another ball and handle the physics."""
        # Calculate distance between ball centers
        dx = other_ball.center_x - self.center_x
        dy = other_ball.center_y - self.center_y
        distance = (dx**2 + dy**2)**0.5

        # Check if balls are overlapping
        if distance < self.radius + other_ball.radius:
            # Calculate collision normal
            if distance == 0:  # Avoid division by zero
                nx, ny = 1, 0
            else:
                nx, ny = dx/distance, dy/distance

            # Calculate relative velocity
            rel_vel_x = self.velocity_x - other_ball.velocity_x
            rel_vel_y = self.velocity_y - other_ball.velocity_y

            # Calculate relative velocity along normal
            rel_vel_normal = rel_vel_x * nx + rel_vel_y * ny

            # Do nothing if balls are moving away from each other
            if rel_vel_normal > 0:
                return

            # Calculate impulse scalar
            e = min(self.elasticity, other_ball.elasticity)
            j = -(1 + e) * rel_vel_normal
            j /= 1/self.mass + 1/other_ball.mass

            # Apply impulse
            impulse_x, impulse_y = j * nx, j * ny

            # Update velocities
            self.velocity_x -= impulse_x / self.mass
            self.velocity_y -= impulse_y / self.mass
            other_ball.velocity_x += impulse_x / other_ball.mass
            other_ball.velocity_y += impulse_y / other_ball.mass

            # Move balls apart to prevent sticking
            overlap = self.radius + other_ball.radius - distance
            self.center_x -= overlap * nx * 0.5
            self.center_y -= overlap * ny * 0.5
            other_ball.center_x += overlap * nx * 0.5
            other_ball.center_y += overlap * ny * 0.5


# Text-based simulation example
def run_text_simulation():
    red_ball = Ball(5, 50, 50, 'Red')
    blue_ball = Ball(color="Blue")
    basic_ball = Ball()
    print(red_ball)
    print(blue_ball)
    print(basic_ball)

    # Example of physics simulation
    print("\nPhysics simulation example:")
    simulation_ball = Ball(radius=15, center_x=100, center_y=50, color="Green")
    simulation_ball.velocity_x = 5
    simulation_ball.apply_gravity(gravity=9.8)

    # Simulate 5 steps
    for i in range(5):
        simulation_ball.update_position(time_step=0.1)
        simulation_ball.check_boundary_collision(width=200, height=200)
        print(f"Step {i+1}: Position=({simulation_ball.center_x:.1f}, {simulation_ball.center_y:.1f}), Velocity=({simulation_ball.velocity_x:.1f}, {simulation_ball.velocity_y:.1f})")


# Visual simulation using Pygame
def run_visual_simulation():
    try:
        import pygame
    except ImportError:
        print("Pygame is not installed. Please install it with: pip install pygame")
        return

    # Initialize pygame
    pygame.init()

    # Set up the display
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Bouncing Balls Simulation")

    # Define colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)

    # Color mapping
    color_map = {
        "Red": RED,
        "Green": GREEN,
        "Blue": BLUE,
        "White": WHITE,
        "Yellow": YELLOW
    }

    # Create balls
    balls = [
        Ball(radius=20, center_x=100, center_y=100, color="Red"),
        Ball(radius=30, center_x=400, center_y=300, color="Blue"),
        Ball(radius=15, center_x=600, center_y=200, color="Green"),
        Ball(radius=25, center_x=300, center_y=400, color="Yellow")
    ]

    # Set initial velocities
    balls[0].velocity_x = 100
    balls[0].velocity_y = -80
    balls[1].velocity_x = -60
    balls[1].velocity_y = 50
    balls[2].velocity_x = 70
    balls[2].velocity_y = 70
    balls[3].velocity_x = -80
    balls[3].velocity_y = -90

    # Set elasticity
    for ball in balls:
        ball.elasticity = 0.9

    # Clock for controlling frame rate
    clock = pygame.time.Clock()
    fps = 60

    # Time step for physics (in seconds)
    time_step = 1.0 / fps

    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Add a new ball on spacebar
                    import random
                    colors = ["Red", "Blue", "Green", "Yellow"]
                    new_ball = Ball(
                        radius=random.randint(10, 30),
                        center_x=random.randint(50, width-50),
                        center_y=random.randint(50, height-50),
                        color=random.choice(colors)
                    )
                    new_ball.velocity_x = random.randint(-100, 100)
                    new_ball.velocity_y = random.randint(-100, 100)
                    new_ball.elasticity = 0.9
                    balls.append(new_ball)

        # Apply gravity to all balls
        for ball in balls:
            ball.apply_gravity(gravity=200)  # Higher gravity for faster simulation

        # Update physics
        for ball in balls:
            ball.update_position(time_step=time_step)
            ball.check_boundary_collision(width=width, height=height)

        # Check for collisions between balls
        for i in range(len(balls)):
            for j in range(i+1, len(balls)):
                balls[i].check_ball_collision(balls[j])

        # Clear the screen
        screen.fill(BLACK)

        # Draw all balls
        for ball in balls:
            pygame_color = color_map.get(ball.color, WHITE)
            pygame.draw.circle(
                screen,
                pygame_color,
                (int(ball.center_x), int(ball.center_y)),
                int(ball.radius)
            )

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(fps)

    # Clean up
    pygame.quit()


if __name__ == "__main__":
    # Uncomment to run the text-based simulation
    # run_text_simulation()

    # Run the visual simulation
    run_visual_simulation()