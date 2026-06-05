#let project(
  title: "",
  author: "",
  university: "",
  department: "",
  degree: "",
  supervisor: "",
  academic_year: "",
  degree_label: "",
  academic_year_label: "",
  logo_path: none,
  numbered_chapters: true,
  heading_numbering: "1.1",
  date: "",
  version: "",
  show_frontespizio: true,
  body
) = {
  // Configurazione base
  set document(title: title, author: author)
  set page(paper: "a4", margin: (inside: 3cm, outside: 2.5cm, top: 3cm, bottom: 3cm))
  set text(font: "New Computer Modern", size: 11pt, lang: "it")
  set par(justify: true, leading: 0.65em)
  
  // Numerazione dei titoli
  set heading(numbering: if heading_numbering != "none" {
    (..nums) => {
      let vals = nums.pos()
      if vals.len() == 1 {
        "Capitolo " + str(vals.at(0)) + ":"
      } else {
        vals.map(str).join(".")
      }
    }
  } else {
    none
  })
  
  // Customizzazione estetica del Titolo del Capitolo
  show heading.where(level: 1): it => {
    set block(above: 1.5em, below: 1em)
    set text(size: 20pt, weight: "bold")
    it
  }
  
  // Impaginazione Frontespizio
  if show_frontespizio {
    align(center)[
      #v(2em)
      #text(size: 18pt, weight: "bold", smallcaps(university))
      #v(1em)
      #text(size: 14pt, department)
      #v(4em)
      #if logo_path != none {
        image(logo_path, width: 30%)
      }
      #v(4em)
      #text(size: 24pt, weight: "bold", title)
      #v(2em)
      #text(size: 14pt, author)
      #v(1fr)
      #text(size: 12pt, date)
    ]
    
    pagebreak()
  }
  
  // Indice
  set page(numbering: "I")
  counter(page).update(1)
  
  outline(title: "Indice", depth: 3, indent: auto)
  
  pagebreak()
  
  // Corpo del testo
  set page(numbering: "1")
  counter(page).update(1)
  
  body
}
