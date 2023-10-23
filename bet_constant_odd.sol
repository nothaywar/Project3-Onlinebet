// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Betting {
    address public admin;
    uint256 public oddsTeamA;
    uint256 public oddsTeamB;
    uint256 public totalBetsTeamA;
    uint256 public totalBetsTeamB;
    enum Outcome { NotDecided, TeamA, TeamB }
    Outcome public outcome = Outcome.NotDecided;
    mapping(address => uint256) public betsTeamA;
    mapping(address => uint256) public betsTeamB;

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can call this function");
        _;
    }

    constructor(uint256 _oddsTeamA, uint256 _oddsTeamB) {
        admin = msg.sender;
        oddsTeamA = _oddsTeamA;
        oddsTeamB = _oddsTeamB;
    }

    function placeBet(bool forTeamA) external payable {
        require(outcome == Outcome.NotDecided, "Betting is closed");
        require(msg.value > 0, "Bet amount must be greater than 0");
        
        if (forTeamA) {
            // Calculate the maximum allowed bet for Team A based on current bets on Team B and odds
            uint256 maxAllowedBetA = (totalBetsTeamB * oddsTeamA) / oddsTeamB;
            require(totalBetsTeamA + msg.value <= maxAllowedBetA, "Betting exceeds allowed odds for Team A");
            
            totalBetsTeamA += msg.value;
            betsTeamA[msg.sender] += msg.value;
        } else {
            // Calculate the maximum allowed bet for Team B based on current bets on Team A and odds
            uint256 maxAllowedBetB = (totalBetsTeamA * oddsTeamB) / oddsTeamA;
            require(totalBetsTeamB + msg.value <= maxAllowedBetB, "Betting exceeds allowed odds for Team B");
            
            totalBetsTeamB += msg.value;
            betsTeamB[msg.sender] += msg.value;
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
            betsTeamA[msg.sender] = 0;  // Reset bet amount to prevent re-entrancy
        } else if (outcome == Outcome.TeamB && betsTeamB[msg.sender] > 0) {
            payout = (betsTeamB[msg.sender] * (totalBetsTeamA + totalBetsTeamB)) / totalBetsTeamB;
            betsTeamB[msg.sender] = 0;  // Reset bet amount to prevent re-entrancy
        }
        require(payout > 0, "No winnings to claim");
        payable(msg.sender).transfer(payout);
    }

    function setOdds(uint256 _oddsTeamA, uint256 _oddsTeamB) external onlyAdmin {
        oddsTeamA = _oddsTeamA;
        oddsTeamB = _oddsTeamB;
    }
}
