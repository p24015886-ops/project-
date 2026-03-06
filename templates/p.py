def maxBridges(northIsland, southIsland):
    n = len(northIsland)

    dp = [[0]*(n+1) for _ in range(n+1)]

    for i in range(1, n+1):
        for j in range(1, n+1):

            if northIsland[i-1] == southIsland[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[n][n]


if __name__ == "__main__":

    n = int(input())

    northIsland = input().split()
    southIsland = input().split()

    result = maxBridges(northIsland, southIsland)

    print(result)