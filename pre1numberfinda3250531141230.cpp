/******************************************************************************

Welcome to GDB Online.
GDB online is an online compiler and debugger tool for C, C++, Python, Java, PHP, Ruby, Perl,
C#, OCaml, VB, Swift, Pascal, Fortran, Haskell, Objective-C, Assembly, HTML, CSS, JS, SQLite, Prolog.
Code, Compile, Run and Debug online from anywhere in world.

*******************************************************************************/

/* #include <iostream>
#include <cstdlib>
#include <ctime>
#include <string>
#include <limits> // numeric_limits
#include <cmath>   // abs, ceil, log2

using namespace std;

int main() {
    srand(time(0));

    while (true) {
        cout << "시작하려면 '시작'을 입력하세요: ";
        string startCommand;
        cin >> startCommand;

        if (startCommand == "시작") {
            int secretNumber = rand() % 19999 - 9999; // -9999 ~ 9999 사이 난수 생성
            int guess;
            int attempts = 0;
            int hintCount = ceil(log2(20000)); // 대략적인 최대 힌트 횟수 (log2(최대 범위))
            int hintsUsed = 0;
            bool canUseHint = true;
            int minRange = -9999;
            int maxRange = 9999;
            bool gameActive = true;

            cout << "-9999부터 9999 사이의 숫자를 맞춰보세요!" << endl;
            cout << "힌트를 사용하려면 '-10000'을 입력하세요. (총 " << hintCount << "번 사용 가능)" << endl;
            cout << "포기하고 싶다면 '10000'을 입력하세요." << endl;

            while (gameActive) {
                cout << "[" << minRange << ", " << maxRange << "] 사이의 숫자를 추측해보세요: ";
                cin >> guess;
                attempts++;

                if (cin.fail()) {
                    cout << "잘못된 입력입니다. 숫자를 입력해주세요." << endl;
                    cin.clear();
                    cin.ignore(numeric_limits<streamsize>::max(), '\n');
                    attempts--;
                    continue;
                }

                if (guess == -10000 && canUseHint) {
                    if (hintsUsed < hintCount) {
                        hintsUsed++;
                        cout << "-- 힌트 (" << hintsUsed << "/" << hintCount << ") --" << endl;
                        if (secretNumber > guess) {
                            minRange = max(minRange, guess + 1);
                            cout << "정답은 " << guess << "보다 큽니다. 범위: [" << minRange << ", " << maxRange << "]" << endl;
                        } else if (secretNumber < guess) {
                            maxRange = min(maxRange, guess - 1);
                            cout << "정답은 " << guess << "보다 작습니다. 범위: [" << minRange << ", " << maxRange << "]" << endl;
                        } else {
                            cout << "정답을 맞추셨으므로 힌트를 사용할 수 없습니다!" << endl;
                            hintsUsed--; // 정답 맞춘 경우는 힌트 사용으로 치지 않음
                        }
                    } else {
                        cout << "더 이상 힌트를 사용할 수 없습니다." << endl;
                    }
                    attempts--; // 힌트 사용 시도는 총 시도 횟수에 포함하지 않음
                    continue;
                } else if (guess == -10000 && !canUseHint) {
                    cout << "힌트 기능이 활성화되지 않았습니다. (활성화하려면 -10000 입력)" << endl;
                    attempts--;
                    continue;
                } else if (guess == 10000) {
                    cout << "포기하시겠습니까? (예/아니오): ";
                    string quitChoice;
                    cin >> quitChoice;
                    if (quitChoice == "예") {
                        cout << "정답은 " << secretNumber << "이었습니다." << endl;
                        gameActive = false;
                    } else {
                        cout << "게임을 계속합니다." << endl;
                        attempts--;
                        continue;
                    }
                } else if (guess > secretNumber) {
                    cout << "DOWN!" << endl;
                } else if (guess < secretNumber) {
                    cout << "UP!" << endl;
                } else {
                    cout << "정답입니다! " << attempts << "번 만에 맞추셨습니다." << endl;
                    gameActive = false;
                }
            }

            cout << "힌트 사용 횟수: " << hintsUsed << " / " << hintCount << "회" << endl;
            cout << "끝내려면 '끝내기', 다시 하려면 '다시하기'를 입력하세요: ";
            string choice;
            cin >> choice;

            if (choice == "끝내기") {
                break;
            } else if (choice != "다시하기") {
                cout << "잘못된 입력입니다. 다시 시작합니다." << endl;
            }
        } else {
            cout << "잘못된 명령어입니다. '시작'을 입력해주세요." << endl;
        }
    }

    cout << "게임을 종료합니다." << endl;
    return 0;
} */

#include <iostream>
#include <cstdlib>
#include <ctime>
#include <string>
#include <limits> // numeric_limits
#include <cmath>   // abs, ceil, log2
#include <algorithm> // max, min

using namespace std;

int main() {
    srand(time(0));

    while (true) {
        cout << "시작하려면 '시작'을 입력하세요: ";
        string startCommand;
        cin >> startCommand;

        if (startCommand == "시작") {
            int secretNumber = rand() % 19999 - 9999; // -9999 ~ 9999 사이 난수 생성
            int guess;
            int attempts = 0;
            int hintCount = ceil(log2(20000)); // 최대 힌트 횟수
            int hintsUsed = 0;
            int chanceCount = 2; // 찬스 횟수
            int chancesUsed = 0;
            int minHintRange = -9999;
            int maxHintRange = 9999;
            bool showRange = false;
            bool gameActive = true;
            int chanceThreshold = 5;

            cout << "-9999부터 9999 사이의 숫자를 맞춰보세요!" << endl;
            cout << "힌트를 사용하려면 '-10000'을 입력하세요. (총 " << hintCount << "번 사용 가능)" << endl;
            cout << "포기하고 싶다면 '10000'을 입력하세요." << endl;
            cout << chanceCount << "번의 찬스로 범위를 확인할 수 있습니다. 많은 시도 후 안내됩니다." << endl;

            while (gameActive) {
                if (showRange) {
                    cout << "[" << minHintRange << ", " << maxHintRange << "] 사이의 숫자를 추측해보세요: ";
                } else {
                    cout << "추측하는 숫자를 입력하세요: ";
                }
                cin >> guess;
                attempts++;

                if (cin.fail()) {
                    cout << "잘못된 입력입니다. 숫자를 입력해주세요." << endl;
                    cin.clear();
                    cin.ignore(numeric_limits<streamsize>::max(), '\n');
                    attempts--;
                    continue;
                }

                if (guess == -10000) {
                    if (hintsUsed < hintCount) {
                        hintsUsed++;
                        cout << "-- 힌트 (" << hintsUsed << "/" << hintCount << ") --" << endl;
                        int rangeSize = maxHintRange - minHintRange + 1;
                        if (rangeSize > 1000) {
                            int step = rangeSize / 4; // 범위를 대략 4단계로 줄여서 보여줌
                            if (secretNumber >= minHintRange && secretNumber < minHintRange + step) {
                                maxHintRange = min(maxHintRange, minHintRange + step - 1);
                                cout << "정답은 " << minHintRange << " 이상 " << minHintRange + step - 1 << " 이하일 수 있습니다." << endl;
                            } else if (secretNumber >= minHintRange + step && secretNumber < minHintRange + 2 * step) {
                                minHintRange = max(minHintRange, minHintRange + step);
                                maxHintRange = min(maxHintRange, minHintRange + 2 * step - 1);
                                cout << "정답은 " << minHintRange << " 이상 " << minHintRange + 2 * step - 1 << " 이하일 수 있습니다." << endl;
                            } else if (secretNumber >= minHintRange + 2 * step && secretNumber < minHintRange + 3 * step) {
                                minHintRange = max(minHintRange, minHintRange + 2 * step);
                                maxHintRange = min(maxHintRange, minHintRange + 3 * step - 1);
                                cout << "정답은 " << minHintRange << " 이상 " << minHintRange + 3 * step - 1 << " 이하일 수 있습니다." << endl;
                            } else {
                                minHintRange = max(minHintRange, minHintRange + 3 * step);
                                cout << "정답은 " << minHintRange << " 이상 " << maxHintRange << " 이하일 수 있습니다." << endl;
                            }
                        } else if (rangeSize > 100) {
                            int step = rangeSize / 2;
                            if (secretNumber >= minHintRange && secretNumber < minHintRange + step) {
                                maxHintRange = min(maxHintRange, minHintRange + step - 1);
                                cout << "정답은 " << minHintRange << " 이상 " << minHintRange + step - 1 << " 이하일 수 있습니다." << endl;
                            } else {
                                minHintRange = max(minHintRange, minHintRange + step);
                                cout << "정답은 " << minHintRange << " 이상 " << maxHintRange << " 이하일 수 있습니다." << endl;
                            }
                        } else {
                            cout << "정답은 " << minHintRange << " 이상 " << maxHintRange << " 이하일 가능성이 높습니다." << endl;
                        }
                    } else {
                        cout << "더 이상 힌트를 사용할 수 없습니다." << endl;
                    }
                    attempts--;
                    continue;
                } else if (guess == 10000) {
                    cout << "포기하시겠습니까? (예/아니오): ";
                    string quitChoice;
                    cin >> quitChoice;
                    if (quitChoice == "예") {
                        cout << "정답은 " << secretNumber << "이었습니다." << endl;
                        gameActive = false;
                    } else {
                        cout << "게임을 계속합니다." << endl;
                        attempts--;
                        continue;
                    }
                } else if (guess > secretNumber) {
                    cout << "DOWN!" << endl;
                } else if (guess < secretNumber) {
                    cout << "UP!" << endl;
                } else {
                    cout << "정답입니다! " << attempts << "번 만에 맞추셨습니다." << endl;
                    gameActive = false;
                }

                if (!gameActive && attempts > 0) break;

                if (attempts >= chanceThreshold && chancesUsed < chanceCount && !showRange) {
                    cout << "벌써 " << attempts << "번 시도하셨습니다. 찬스를 사용해 현재 범위를 확인하시겠습니까? (" << chanceCount - chancesUsed << "번 남음) (예/아니오): ";
                    string useChance;
                    cin >> useChance;
                    if (useChance == "예") {
                        showRange = true;
                        chancesUsed++;
                        cout << "-- 찬스 사용 (" << chancesUsed << "/" << chanceCount << ") --" << endl;
                        cout << "현재 추측 범위: [" << minHintRange << ", " << maxHintRange << "]" << endl;
                    }
                }
            }

            cout << "힌트 사용 횟수: " << hintsUsed << " / " << hintCount << "회" << endl;
            cout << "찬스 사용 횟수: " << chancesUsed << " / " << chanceCount << "회" << endl;
            cout << "끝내려면 '끝내기', 다시 하려면 '다시하기'를 입력하세요: ";
            string choice;
            cin >> choice;

            if (choice == "끝내기") {
                break;
            } else if (choice != "다시하기") {
                cout << "잘못된 입력입니다. 다시 시작합니다." << endl;
            }
        } else {
            cout << "잘못된 명령어입니다. '시작'을 입력해주세요." << endl;
        }
    }

    cout << "게임을 종료합니다." << endl;
    return 0;
}
