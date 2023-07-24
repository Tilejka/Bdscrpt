let enlarged = false;
const img = document.getElementById("world-image");

function toggleImageSize() {
  if (enlarged) {
    img.style.transform = "scale(1)";
    img.style.transition = "transform 0.25s ease";
    img.style.position = "static";
    img.style.zIndex = "auto";
    enlarged = false;
  } else {
    const imageWidth = img.width;
    const imageHeight = img.height;
    const pageWidth = window.innerWidth;
    const pageHeight = window.innerHeight;

    const scaleWidth = pageWidth / imageWidth;
    const scaleHeight = pageHeight / imageHeight;
    const scale = Math.min(scaleWidth, scaleHeight);

    img.style.transform = `scale(${scale})`;
    img.style.transition = "transform 0.25s ease";
    img.style.position = "fixed";
    img.style.zIndex = "9999";
    img.style.left = "50%";
    img.style.top = "50%";
    img.style.transformOrigin = "center";
    img.style.transform = "translate(-50%, -50%)";
    enlarged = true;
  }
}

img.addEventListener('click', toggleImageSize);
