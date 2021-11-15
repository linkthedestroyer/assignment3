function disableEnableImages() {
  const images = document.getElementsByName("image");
  for (const image of images) {
    if (image.getAttribute("class")?.indexOf("hide") >= 0) {
      $(image).removeClass("hide");
    } else {
      $(image).addClass("hide");
    }
  }
  const card_text_list = document.getElementsByName("card_text");
  for (const card_text of card_text_list) {
    if (card_text.getAttribute("class")?.indexOf("card-image-and-text") >= 0) {
      $(card_text).addClass("card-just-text");
      $(card_text).removeClass("card-image-and-text");
    } else {
      $(card_text).removeClass("card-just-text");
      $(card_text).addClass("card-image-and-text");
    }
  }
}
function disableText() {
  const textRows = document.getElementsByClassName("text-row");
  for (const textRow of textRows) {
    if (textRow.hasAttribute("style")) {
      textRow.removeAttribute("style");
    } else {
      textRow.setAttribute("style", "display: None;");
    }
  }
  const detailRows = document.getElementsByClassName("detail-row");
  for (const detailRow of detailRows) {
    if (detailRow.getAttribute("class")?.indexOf("skip-border") >= 0) {
      $(detailRow).removeClass("skip-border");
    } else {
      $(detailRow).addClass("skip-border");
    }
  }
}
function showAll() {
  let rows = document.getElementsByClassName("detail-row");
  for (const row of rows) {
    $(row).removeClass("hide");
  }
  rows = document.getElementsByClassName("text-row");
  for (const row of rows) {
    $(row).removeClass("hide");
  }
}
function yoursOnly() {
  let rows = document.getElementsByName("yours");
  for (const row of rows) {
    $(row).removeClass("hide");
  }
  rows = document.getElementsByName("not-yours");
  for (const row of rows) {
    $(row).addClass("hide");
  }
}
function notYoursOnly() {
  let rows = document.getElementsByName("yours");
  for (const row of rows) {
    $(row).addClass("hide");
  }
  1;
  rows = document.getElementsByName("not-yours");
  for (const row of rows) {
    $(row).removeClass("hide");
  }
}
function checkrow(rowId) {
  const checkbox = document.getElementById(`${rowId}`);
  if (checkbox) {
    checkbox.checked = !checkbox.checked;
    checkbox.onchange();
  }
}
