export default [
  {
    "id": 0,
    "payoutMultiplier": 30,
    "events": [
      {
        "index": 0,
        "type": "reveal",
        "board": [
          [
            {
              "name": "H3"
            },
            {
              "name": "L1"
            },
            {
              "name": "L4"
            },
            {
              "name": "H5"
            },
            {
              "name": "H3"
            },
            {
              "name": "H4"
            },
            {
              "name": "L4"
            }
          ],
          [
            {
              "name": "H4"
            },
            {
              "name": "L1"
            },
            {
              "name": "L2"
            },
            {
              "name": "H5"
            },
            {
              "name": "H4"
            },
            {
              "name": "L4"
            },
            {
              "name": "L2"
            }
          ],
          [
            {
              "name": "L4"
            },
            {
              "name": "L1"
            },
            {
              "name": "H3"
            },
            {
              "name": "H5"
            },
            {
              "name": "L4"
            },
            {
              "name": "L2"
            },
            {
              "name": "H3"
            }
          ],
          [
            {
              "name": "L2"
            },
            {
              "name": "L1"
            },
            {
              "name": "H4"
            },
            {
              "name": "H5"
            },
            {
              "name": "L2"
            },
            {
              "name": "H3"
            },
            {
              "name": "H4"
            }
          ],
          [
            {
              "name": "H3"
            },
            {
              "name": "L1"
            },
            {
              "name": "L4"
            },
            {
              "name": "H5"
            },
            {
              "name": "H3"
            },
            {
              "name": "H4"
            },
            {
              "name": "L4"
            }
          ]
        ],
        "paddingPositions": [
          12,
          16,
          6,
          16,
          46
        ],
        "gameType": "basegame",
        "anticipation": [
          0,
          0,
          0,
          0,
          0
        ]
      },
      {
        "index": 1,
        "type": "matchDuelReveal",
        "reelIndex": 4,
        "multiplier": 7
      },
      {
        "index": 2,
        "type": "winInfo",
        "totalWin": 30,
        "wins": [
          {
            "symbol": "L1",
            "kind": 3,
            "win": 10,
            "positions": [
              {
                "reel": 0,
                "row": 0
              },
              {
                "reel": 1,
                "row": 0
              },
              {
                "reel": 2,
                "row": 0
              },
              {
                "reel": 3,
                "row": 0
              },
              {
                "reel": 4,
                "row": 0
              }
            ],
            "meta": {
              "lineIndex": 1,
              "multiplier": 1,
              "winWithoutMult": 10,
              "globalMult": 1,
              "lineMultiplier": 1
            }
          },
          {
            "symbol": "H5",
            "kind": 3,
            "win": 20,
            "positions": [
              {
                "reel": 0,
                "row": 2
              },
              {
                "reel": 1,
                "row": 2
              },
              {
                "reel": 2,
                "row": 2
              },
              {
                "reel": 3,
                "row": 2
              },
              {
                "reel": 4,
                "row": 2
              }
            ],
            "meta": {
              "lineIndex": 3,
              "multiplier": 1,
              "winWithoutMult": 20,
              "globalMult": 1,
              "lineMultiplier": 1
            }
          }
        ]
      },
      {
        "index": 3,
        "type": "setWin",
        "amount": 30,
        "winLevel": 5
      },
      {
        "index": 4,
        "type": "setTotalWin",
        "amount": 30
      },
      {
        "index": 5,
        "type": "finalWin",
        "amount": 30
      }
    ],
    "criteria": "basegame",
    "baseGameWins": 42.2,
    "freeGameWins": 0.0
  }
];
