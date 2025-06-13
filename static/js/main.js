document.addEventListener("DOMContentLoaded", () => {
  // Smooth scrolling for navigation links
  document.querySelectorAll("a[data-smooth-scroll]").forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()

      const targetId = this.getAttribute("href")
      const targetElement = document.querySelector(targetId)

      if (targetElement) {
        // Close mobile menu if open
        const offCanvas = document.querySelector("#mobile-menu")
        if (offCanvas && offCanvas.classList.contains("is-open")) {
          window.Zepto(offCanvas).foundation("close")
        }

        // Scroll to target
        window.scrollTo({
          top: targetElement.offsetTop - 80, // Adjust for fixed header
          behavior: "smooth",
        })
      }
    })
  })

  // Navbar scroll effect
  const navbar = document.querySelector(".top-bar")
  window.addEventListener("scroll", () => {
    if (window.scrollY > 50) {
      navbar.classList.add("scrolled")
    } else {
      navbar.classList.remove("scrolled")
    }
  })

  // Project filter active state
  const filterLinks = document.querySelectorAll(".project-filter a")
  filterLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault()
      filterLinks.forEach((l) => l.classList.remove("active"))
      this.classList.add("active")
    })
  })

  // Lazy loading images
  if ("loading" in HTMLImageElement.prototype) {
    // Browser supports native lazy loading
    const lazyImages = document.querySelectorAll('img[loading="lazy"]')
    lazyImages.forEach((img) => {
      img.src = img.dataset.src
    })
  } else {
    // Fallback for browsers that don't support native lazy loading
    const lazyImageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const lazyImage = entry.target
          lazyImage.src = lazyImage.dataset.src
          lazyImageObserver.unobserve(lazyImage)
        }
      })
    })

    const lazyImages = document.querySelectorAll("img[data-src]")
    lazyImages.forEach((img) => {
      lazyImageObserver.observe(img)
    })
  }

  // Simple parallax effect
  const parallaxElements = document.querySelectorAll(".parallax")
  window.addEventListener("scroll", () => {
    const scrollTop = window.pageYOffset

    parallaxElements.forEach((element) => {
      const speed = element.dataset.speed || 0.5
      element.style.transform = `translateY(${scrollTop * speed}px)`
    })
  })

  // Initialize Foundation
  window.Zepto(document).foundation()
})

// HTMX events
document.addEventListener("htmx:afterSwap", (event) => {
  // Reinitialize Foundation components after HTMX content swap
  if (event.detail.target.id === "project-modal-content") {
    window.Zepto("#project-modal").foundation("open")
  }

  // Reinitialize Foundation form validation
  if (event.detail.target.id === "contact-form-container") {
    window.Zepto(document).foundation()

    // Scroll to success message if present
    const successMessage = document.querySelector(".callout.success")
    if (successMessage) {
      successMessage.scrollIntoView({ behavior: "smooth", block: "center" })
    }
  }
})

document.addEventListener("htmx:beforeSend", (event) => {
  // Form validation before HTMX request
  if (event.detail.elt.tagName === "FORM") {
    const form = event.detail.elt
    const isValid = form.checkValidity()

    if (!isValid) {
      event.preventDefault()
      // Trigger HTML5 validation UI
      form.reportValidity()
    }
  }
})

// Add response status handling
document.addEventListener("htmx:responseError", (event) => {
  const errorContainer = document.getElementById("form-messages")
  if (errorContainer) {
    errorContainer.innerHTML = `
      <div class="callout alert">
        <h5>Error</h5>
        <p>There was a problem submitting your form. Please try again later.</p>
      </div>
    `
    errorContainer.scrollIntoView({ behavior: "smooth", block: "center" })
  }
})
