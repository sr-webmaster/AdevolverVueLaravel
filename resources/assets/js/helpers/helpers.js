const isMenuArea = event => {
  if(event.relatedTarget === null) {
    return false;
  }

  if(event.relatedTarget.className === 'menu-area' ) {
    return true
  } else {
    return false
  }
}

export const isBottom = () => {
  const scrollY = window.scrollY
  const visible = document.documentElement.clientHeight
  const pageHeight = document.documentElement.scrollHeight
  const bottomOfPage = visible + scrollY >= pageHeight
  return bottomOfPage || pageHeight < visible
}

export default isMenuArea