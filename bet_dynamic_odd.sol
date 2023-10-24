// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Betting {
    address public admin;
    address public feeRecipient;
    enum Outcome { NotDecided, TeamA, TeamB }
    Outcome public outcome = Outcome.NotDecided;
    mapping(address => uint256) public betsTeamA;
    mapping(address => uint256) public betsTeamB;
    uint256 public totalBetsTeamA;
    uint256 public totalBetsTeamB;
    bool public bettingOpen = true;  // Control if bet is open

    constructor(address _feeRecipient) {
        admin = msg.sender;
        feeRecipient = _feeRecipient;
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can call this function");
        _;
    }

    // Admin can open or close betting
    function toggleBetting(bool open) external onlyAdmin {
        bettingOpen = open;
    }

    function placeBet(bool forTeamA) external payable {
        require(bettingOpen, "Betting is closed");  // Check if the bet is close
        require(outcome == Outcome.NotDecided, "Outcome already decided");
        require(msg.value > 0, "Bet amount must be greater than 0");
        
        uint256 fee = msg.value / 100;
        uint256 betAmount = msg.value - fee;
        
        payable(feeRecipient).transfer(fee);
        
        if (forTeamA) {
            betsTeamA[msg.sender] += betAmount;
            totalBetsTeamA += betAmount;
        } else {
            betsTeamB[msg.sender] += betAmount;
            totalBetsTeamB += betAmount;
        }
    }

    // Admin can withdraw ETH from pool
    function withdraw(uint256 amount) external onlyAdmin {
        require(amount <= address(this).balance, "Amount exceeds contract balance");
        payable(admin).transfer(amount);
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

    function getTotalBets() external view returns (uint256 totalBetsA, uint256 totalBetsB) {
        return (totalBetsTeamA, totalBetsTeamB);
    }

    function getBetDetails(address bettor) external view returns (uint256 betTeamA, uint256 betTeamB) {
        return (betsTeamA[bettor], betsTeamB[bettor]);
    }

    function getOutcome() external view returns (Outcome) {
        return outcome;
    }

    function getAdmins() external view returns (address contractAdmin, address feeReceiver) {
        return (admin, feeRecipient);
    }
}
