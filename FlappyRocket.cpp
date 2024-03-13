#include <iostream>
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>
#include <vector>
#include <random>

const int windowHeight = 20;
const int windowWidth = 40;
const int birdX = 10;
float birdY = windowHeight / 2.0f;
const float gravity = 0.4f;
const float jumpStrength = 1.5f; // Adjust the jump strength as needed

const char birdChar = 'o';
const char groundChar = '-';
const char emptyChar = ' ';

// Define the 2D array for the circle
const int circleSize = 9;
const char circle[circleSize][circleSize + 9] = {
    "      * * *     ",
    "   *         *   ",
    " *             * ",
    "*               *",
    "*               *",
    "*               *",
    " *             * ",
    "   *         *   ",
    "      * * *      "
};

int getch() {
    struct termios oldt, newt;
    int ch;
    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);
    ch = getchar();
    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    return ch;
}

int kbhit() {
    struct termios oldt, newt;
    int ch;
    int oldf;
    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);
    oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
    fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);
    ch = getchar();
    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    fcntl(STDIN_FILENO, F_SETFL, oldf);
    if (ch != EOF) {
        ungetc(ch, stdin);
        return 1;
    }
    return 0;
}

bool checkCollision(const std::vector<int>& circlePositions, int verticalDistance) {
    // Calculate the center position of the bird
    float birdCenterX = birdX;
    float birdCenterY = birdY + verticalDistance + 0.5f; // Add 0.5 to get the center of the 'o' character

    // Check if the bird collides with any of the circles based on their centers
    for (int circleX : circlePositions) {
        // Calculate the center position of the current circle
        float circleCenterX = circleX + (circleSize + 9) / 2.0f;
        float circleCenterY = windowHeight / 2.0f + verticalDistance + circleSize / 2.0f;

        // Calculate the distance between the centers of the bird and the circle
        float distanceX = birdCenterX - circleCenterX;
        float distanceY = birdCenterY - circleCenterY;
        float distance = std::sqrt(distanceX * distanceX + distanceY * distanceY);

        // Check if the distance is less than the sum of the radii (circleSize/2) to detect collision
        if (distance < circleSize / 2.0f) {
            return true; // Collision detected
        }
    }
    return false; // No collision
}

void drawGame(const std::vector<int>& circlePositions, const std::vector<int>& verticalDistances) {
    system("clear"); // Clear the console
    for (int y = 0; y < windowHeight; y++) {
        for (int x = 0; x < windowWidth; x++) {
            if (y == static_cast<int>(birdY) && x == birdX) {
                std::cout << birdChar; // Draw the bird
            } else if (y == windowHeight - 1) {
                std::cout << groundChar; // Draw the ground
            } else {
                bool drawn = false;
                for (size_t i = 0; i < circlePositions.size(); i++) {
                    int circleX = circlePositions[i];
                    int verticalDistance = verticalDistances[i];
                    if (y >= windowHeight / 2 - verticalDistance && y < windowHeight / 2 + circleSize - verticalDistance &&
                        x >= circleX && x < circleX + circleSize + 9) {
                        int circleY = y - (windowHeight / 2 - verticalDistance);
                        int circleXPos = x - circleX;
                        std::cout << circle[circleY][circleXPos]; // Draw the circle
                        drawn = true;
                        break;
                    }
                }
                if (!drawn) {
                    std::cout << emptyChar; // Draw empty space
                }
            }
        }
        std::cout << std::endl;
    }
}

int main() {
    char ch;
    bool gameOver = false;
    std::vector<int> circlePositions;
    std::vector<int> verticalDistances;
    
    //random values
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(1, 12);

    while (!gameOver) {
        // Get input character
        if (kbhit()) {
            ch = getch();
        } else {
            ch = '\0'; // Set ch to a default value if no input
        }

        // Handle 'w' key input for jump
        if (ch == 'w') {
            // Move the bird up on 'w' key press
            birdY -= jumpStrength;
        }

        // Apply gravity to the bird
        birdY += gravity;

        // Check if the bird goes above the frame
        if (birdY < 0) {
            birdY = 0;
        }

        // Check for collision with the ground or any of the circles
        if (birdY >= windowHeight - 1 || (!circlePositions.empty() && checkCollision(circlePositions, verticalDistances[0]))) {
            birdY = windowHeight - 1;
            gameOver = true;
        }

        // Move the circle toward the left
        for (size_t i = 0; i < circlePositions.size(); i++) {
            circlePositions[i]--;
            if (circlePositions[i] + circleSize + 9 <= 0) {
                // Remove the circle if it's completely off the screen
                circlePositions.erase(circlePositions.begin() + i);
                verticalDistances.erase(verticalDistances.begin() + i);
                i--;
            }
        }

        // Add a new circle if needed
        if (circlePositions.empty() || windowWidth - circlePositions.back() >= 25) {
            circlePositions.push_back(windowWidth - 1);
            verticalDistances.push_back(dis(gen));
        }

        // Draw the game to render the bird and circles
        drawGame(circlePositions, verticalDistances);

        // Add a small delay to control game speed
        usleep(100000);
    }

    std::cout << "Game Over!" << std::endl;

    return 0;
}
