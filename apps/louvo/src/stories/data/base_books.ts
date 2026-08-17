export default [
  {
    "id": 0,
    "payoutMultiplier": 24,
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
              "name": "H4"
            },
            {
              "name": "L4"
            },
            {
              "name": "H5"
            },
            {
              "name": "L1"
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
              "name": "H4"
            },
            {
              "name": "L4"
            },
            {
              "name": "H3"
            },
            {
              "name": "H5"
            },
            {
              "name": "L2"
            },
            {
              "name": "L1"
            },
            {
              "name": "H4"
            }
          ],
          [
            {
              "name": "L4"
            },
            {
              "name": "H3"
            },
            {
              "name": "H4"
            },
            {
              "name": "H5"
            },
            {
              "name": "L1"
            },
            {
              "name": "L2"
            },
            {
              "name": "L4"
            }
          ],
          [
            {
              "name": "H3"
            },
            {
              "name": "H4"
            },
            {
              "name": "L4"
            },
            {
              "name": "H5"
            },
            {
              "name": "L2"
            },
            {
              "name": "L1"
            },
            {
              "name": "H3"
            }
          ],
          [
            {
              "name": "H4"
            },
            {
              "name": "L4"
            },
            {
              "name": "H3"
            },
            {
              "name": "H5"
            },
            {
              "name": "L1"
            },
            {
              "name": "L2"
            },
            {
              "name": "H4"
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
        "totalWin": 24,
        "wins": [
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
          },
          {
            "symbol": "L2",
            "kind": 3,
            "win": 2,
            "positions": [
              {
                "reel": 0,
                "row": 4
              },
              {
                "reel": 1,
                "row": 3
              },
              {
                "reel": 2,
                "row": 4
              },
              {
                "reel": 3,
                "row": 3
              },
              {
                "reel": 4,
                "row": 4
              }
            ],
            "meta": {
              "lineIndex": 13,
              "multiplier": 1,
              "winWithoutMult": 2,
              "globalMult": 1,
              "lineMultiplier": 1
            }
          },
          {
            "symbol": "L1",
            "kind": 3,
            "win": 2,
            "positions": [
              {
                "reel": 0,
                "row": 3
              },
              {
                "reel": 1,
                "row": 4
              },
              {
                "reel": 2,
                "row": 3
              },
              {
                "reel": 3,
                "row": 4
              },
              {
                "reel": 4,
                "row": 3
              }
            ],
            "meta": {
              "lineIndex": 9,
              "multiplier": 1,
              "winWithoutMult": 2,
              "globalMult": 1,
              "lineMultiplier": 1
            }
          }
        ]
      },
      {
        "index": 3,
        "type": "setWin",
        "amount": 24,
        "winLevel": 5
      },
      {
        "index": 4,
        "type": "setTotalWin",
        "amount": 24
      },
      {
        "index": 5,
        "type": "finalWin",
        "amount": 24
      }
    ],
    "criteria": "basegame",
    "baseGameWins": 42.2,
    "freeGameWins": 0.0
  }
];
