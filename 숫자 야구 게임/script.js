let attempts = 9;        
let answer = [];         
let isGameOver = false;

const input1 = document.getElementById("number1");
const input2 = document.getElementById("number2");
const input3 = document.getElementById("number3");

const attemptsEl = document.getElementById("attempts");
const resultsEl = document.getElementById("results");
const resultImgEl = document.getElementById("game-result-img");
const submitBtn = document.querySelector(".submit-button");

function clearInputs(focusFirst = false) {
  input1.value = "";
  input2.value = "";
  input3.value = "";
  if (focusFirst) input1.focus();
}

function makeAnswer() {
  const nums = [];
  while (nums.length < 3) {
    const n = Math.floor(Math.random() * 10);
    if (!nums.includes(n)) nums.push(n);
  }
  return nums;
}

function initGame() {
  attempts = 9;
  answer = makeAnswer();
  isGameOver = false;

  attemptsEl.textContent = String(attempts);
  resultsEl.innerHTML = "";
  resultImgEl.src = "";
  resultImgEl.alt = "";

  submitBtn.disabled = false;
  clearInputs(true);    
}

function getGuess() {
  const v1 = input1.value.trim();
  const v2 = input2.value.trim();
  const v3 = input3.value.trim();

  if (v1 === "" || v2 === "" || v3 === "") {
    clearInputs(true);
    return null;
  }

  return [Number(v1), Number(v2), Number(v3)];
}

function calcResult(guess, ans) {
  let strike = 0;
  let ball = 0;

  for (let i = 0; i < 3; i++) {
    if (guess[i] === ans[i]) strike++;
    else if (ans.includes(guess[i])) ball++;
  }
  const out = (strike === 0 && ball === 0);
  return { strike, ball, out };
}

function appendResultRow(guess, result) {
  const row = document.createElement("div");
  row.className = "check-result";

  const left = document.createElement("div");
  left.className = "left";
  left.innerHTML = `
    <span class="num-result">${guess[0]}</span>
    <span class="num-result">${guess[1]}</span>
    <span class="num-result">${guess[2]}</span>
  `;

  const right = document.createElement("div");
  right.className = "right";

  if (result.out) {
    right.innerHTML = `<span class="num-result out">O</span>`;
  } else {
    const s = `${result.strike} <span class="num-result strike">S</span>`;
    const b = `${result.ball} <span class="num-result ball">B</span>`;
    right.innerHTML = `${s} ${b}`;
  }
  
  row.style.display = "flex";
  row.style.justifyContent = "space-between";
  row.style.alignItems = "center";

  const mid = document.createElement("div");
  mid.textContent = ":";
  mid.style.margin = "0 16px";
  mid.style.fontWeight = "bold";

  row.appendChild(left);
  row.appendChild(mid);
  row.appendChild(right);

  resultsEl.append(row);
}

function endGame(win) {
  isGameOver = true;
  submitBtn.disabled = true;

  resultImgEl.src = win ? "./success.png" : "./fail.png";
  resultImgEl.alt = win ? "success" : "fail";
}

window.check_numbers = function check_numbers() {
  if (isGameOver) return;

  const guess = getGuess();
  if (!guess) return;

  attempts -= 1;
  attemptsEl.textContent = String(attempts);

  const result = calcResult(guess, answer);
  appendResultRow(guess, result);

  clearInputs(true);

  if (result.strike === 3) {
    endGame(true);
    return;
  }

  if (attempts <= 0) {
    endGame(false);
  }

};

initGame();
