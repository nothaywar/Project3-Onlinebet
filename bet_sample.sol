// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Betting {
    address public admin;
    enum Outcome { NotDecided, TeamA, TeamB }
    Outcome public outcome = Outcome.NotDecided;
    mapping(address => uint256) public betsTeamA;
    mapping(address => uint256) public betsTeamB;
    uint256 public totalBetsTeamA;
    uint256 public totalBetsTeamB;

    constructor() {
        admin = msg.sender;
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can call this function");
        _;
    }

    function placeBet(bool forTeamA) external payable {
        require(outcome == Outcome.NotDecided, "Betting is closed");
        require(msg.value > 0, "Bet amount must be greater than 0");
        if (forTeamA) {
            betsTeamA[msg.sender] += msg.value;
            totalBetsTeamA += msg.value;
        } else {
            betsTeamB[msg.sender] += msg.value;
            totalBetsTeamB += msg.value;
        }
    }

    function decideOutcome(bool teamAWon) external onlyAdmin {
        require(outcome == Outcome.NotDecided, "Outcome already decided");
        outcome = teamAWon ? Outcome.TeamA : Outcome.TeamB;
    }

    function claimWinnings() external {
        require(outcome != Outcome.NotDecided, "Outcome not decided yet");
        uint256 payout = 0;
        if (outcome == Outcome.TeamA && betsTeamA[msg.sender] > 0) {
            payout = (betsTeamA[msg.sender] * (totalBetsTeamA + totalBetsTeamB)) / totalBetsTeamA;
        } else if (outcome == Outcome.TeamB && betsTeamB[msg.sender] > 0) {
            payout = (betsTeamB[msg.sender] * (totalBetsTeamA + totalBetsTeamB)) / totalBetsTeamB;
        }
        require(payout > 0, "No winnings to claim");
        payable(msg.sender).transfer(payout);
    }
}
