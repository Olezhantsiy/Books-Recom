/* DOM */
const scoreInput = document.getElementById('score')
const scorediv = document.getElementById('scorediv')
/* END DOM */

const score = roundToHalf(scoreInput.value)

const scoreFloor = Math.floor(score)

const scoreRest = score - scoreFloor

const scoreEmpty = 5 - Math.ceil(score)

for (let i = 0; i < scoreFloor; i++) {
    scorediv.insertAdjacentHTML('beforeend', `
        <img src="/static/images/star_full.svg" alt="star" class="star_info" style="width: 1.3rem">
    `)
}

for (let i = 0; i < scoreRest; i+=0.5) {
    scorediv.insertAdjacentHTML('beforeend', `
        <img src="/static/images/star_half.svg" alt="star" class="star_info" style="width: 1.3rem"> 
    `)
}

for (let i = 0; i < scoreEmpty; i++) {
    scorediv.insertAdjacentHTML('beforeend', `
        <img src="/static/images/star_empty.svg" alt="star" class="star_info" style="width: 1.3rem">
    `)
}

function roundToHalf(num) {
    return Math.round(num * 2) / 2;
}