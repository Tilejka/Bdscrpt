function toggleImageSize() {
  const image = document.getElementById('world-image');
  if (image.style.width === '100%') {
    image.style.width = 'auto';
  } else {
    image.style.width = '100%';
  }
}
