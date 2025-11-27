const totalFrames = 6572;
const jsonDir = "http://localhost:8000/"
const delay = 33;
const TARGET_W = 640.86;
const TARGET_H = 360;

const pathEl = document.querySelector('.line-chart__line');
if (!pathEl) {
  console.error('Cannot find .line-chart__line on this page.');
} else {
  const svg = pathEl.closest('svg');
  if (!svg) {
    console.error('Found path but not its parent SVG.');
  } else {
    const wrapper = document.createElement('div');
    wrapper.className = 'ba-animation-wrapper';
    Object.assign(wrapper.style, {
      height: TARGET_H + 'px',
      minHeight: TARGET_H + 'px',
      display: 'block',
      boxSizing: 'border-box',
      position: 'relative',
      overflow: 'visible',
      zIndex: 1
    });

    const svgParent = svg.parentElement;
    svgParent.insertBefore(wrapper, svg);
    wrapper.appendChild(svg);

    svg.setAttribute('height', TARGET_H);
    svg.style.height = TARGET_H + 'px';
    const vb = svg.getAttribute('viewBox');
    if (!vb) {
      svg.setAttribute('viewBox', `0 $${TARGET_H}`);
    }

    let cur = wrapper.parentElement;
    let steps = 0;
    while (cur && cur !== document.body && steps < 12) {
      const cs = window.getComputedStyle(cur);
      if (cs.display.includes('flex') || cs.display.includes('grid')) {
        cur.style.flex = cur.style.flex || '0 0 auto';
      }
      cur.style.maxHeight = cur.style.maxHeight || 'none';
      if (cs.overflow !== 'visible') cur.style.overflow = 'visible';
      cur.style.minHeight = cur.style.minHeight || TARGET_H + 'px';

      cur = cur.parentElement;
      steps++;
    }
  }
}

const pathElement = document.querySelector(".line-chart__line");
const svgElement = pathElement.closest("svg");

svgElement.setAttribute("width", TARGET_W);
svgElement.setAttribute("height", TARGET_H);
svgElement.style.width = TARGET_W + "px";
svgElement.style.height = TARGET_H + "px";

svgElement.setAttribute("viewBox", `0 0 ${TARGET_W} ${TARGET_H}`);

function loadFrame(i) {
  const name = `frame_${i.toString().padStart(4, "0")}.json`;

  return fetch(jsonDir + name)
    .then(r => r.json())
    .then(data => {
      pathElement.setAttribute("d", data.path);
    })
    .catch(err => console.error("Frame error:", name, err));
}

async function play() {
  for (let i = 0; i < totalFrames; i++) {
    await loadFrame(i);
    await new Promise(r => setTimeout(r, delay));
  }
}

play();
