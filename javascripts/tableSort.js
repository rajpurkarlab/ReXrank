function sortTable(columnIndex, button) {
    const table = document.getElementById("modelTable");
    let rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    switching = true;
    dir = "desc"; 
  
    while (switching) {
      switching = false;
      rows = table.rows;
  
      for (i = 1; i < (rows.length - 1); i++) {
        shouldSwitch = false;
        x = rows[i].getElementsByTagName("TD")[columnIndex - 1];
        y = rows[i + 1].getElementsByTagName("TD")[columnIndex - 1];
  
        if (dir == "desc") {
          if (parseFloat(x.innerHTML) < parseFloat(y.innerHTML)) {
            shouldSwitch = true;
            break;
          }
        } else if (dir == "asc") {
          if (parseFloat(x.innerHTML) > parseFloat(y.innerHTML)) {
            shouldSwitch = true;
            break;
          }
        }
      }
  
      if (shouldSwitch) {
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
        switchcount++;
      } else {
        if (switchcount == 0 && dir == "desc") {
          dir = "asc";
          switching = true;
        }
      }
    }
  
    // Reset all button colors
    const buttons = document.querySelectorAll('.sort-button');
    buttons.forEach(btn => btn.classList.remove('active'));
    // Set the clicked button to active
    button.classList.add('active');
  }
  
  // Initial sorting by RadGraph (4th column)
  document.addEventListener('DOMContentLoaded', () => {
    sortTable(4, document.querySelectorAll('.sort-button')[2]);
  });
  