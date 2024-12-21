function randomGen() {
  let min = 100000
  let max = 1000000
  return (Math.floor((Math.random())*(max-min+1))+min).toString();
}



// Toast Alert
const toastBox = document.querySelector('#toast-box')
function showToast(toastID, username, msg, img) {
    if (img == '') {
      img = default_img_profile
    }
  html = `

    <!-- Then put toasts within -->
    <div class="toast" role="alert" id="toast${toastID}" aria-live="assertive" aria-atomic="true">
      <div class="toast-header">
        <img src="${img}" class="rounded me-2" alt="..." width="50" style="border-radius: 100% !important;">
        <strong class="me-auto">${username}</strong>
        <small class="text-body-secondary">الان</small>
        <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
      <div class="toast-body">
        ${msg}
      </div>
    </div>
  `


  toastBox.insertAdjacentHTML("beforeend", html)
  $(`#toast${toastID}`).toast('show');

};





// add bootstrap forms-control
const forms = document.querySelectorAll('.FormAuto')
forms.forEach(form=>{

  if (form) {
    let inputs = form.querySelectorAll('input, textarea, select')
    inputs.forEach(el => {
      let label = form.querySelector(`label[for="${el.id}"]`)
      box_class = ''
      help_text = ''
      error_text = ''
      help_text_el = form.querySelector(`#${el.id}_helptext`)
      error_text_el = form.querySelector(`#${el.id}_error`)
      if (help_text_el) {
        help_text_el.remove()
        help_text = help_text_el.outerHTML
      }
      if (error_text_el) {
        error_text_el.remove()
        error_text = error_text_el.outerHTML
      }

      if (label) {
        if (el.tagName == 'SELECT') {
          el.classList.add('form-select')
          label.classList.add('form-label')
          box_class += 'mb-3 '
  
        } else {
          if (el.type == 'checkbox') {
            el.classList.add('form-check-input')
            if (form.classList.contains('check-cols')) {
              box_class += 'form-check form-switch mb-3 col'
            } else {
              box_class += 'form-check form-switch mb-3 w-100'
            }
          } else {
            el.classList.add('form-control')
            label.classList.add('form-label')
            if (el.tagName != 'TEXTAREA') {
              box_class += 'mb-3 col'
            } else {
              box_class += 'mb-3 w-100'
            }
  
          }
        }

        
        label.insertAdjacentHTML('beforebegin', `<div class="${box_class}">${label.outerHTML+error_text+el.outerHTML+help_text}</div>`)
        el.remove()
        label.remove()
      }
  
    })
  }  
})
