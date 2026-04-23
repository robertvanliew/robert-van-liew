/* ============================================================
   Robert Vanliew — Portfolio Scripts
   Scroll animations, nav toggle, smooth scroll
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
  // ---------- Elements ----------
  const hamburger = document.getElementById('hamburger');
  const folderTabs = document.getElementById('folderTabs');
  const backToTop = document.getElementById('backToTop');
  const reveals = document.querySelectorAll('.reveal');
  const navAnchors = document.querySelectorAll('.nav-link[href^="#"]');

  // ---------- Scroll-triggered Reveal Animations ----------
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          revealObserver.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.15,
      rootMargin: '0px 0px -40px 0px',
    }
  );

  reveals.forEach((el) => revealObserver.observe(el));

  // ---------- Navbar Scroll Effect ----------
  let lastScroll = 0;

  function handleNavScroll() {
    const scrollY = window.scrollY;

    // Back to top button
    if (scrollY > 600) {
      backToTop.classList.add('visible');
    } else {
      backToTop.classList.remove('visible');
    }

    lastScroll = scrollY;
  }

  // Throttle scroll handler
  let scrollTicking = false;
  window.addEventListener('scroll', () => {
    if (!scrollTicking) {
      window.requestAnimationFrame(() => {
        handleNavScroll();
        scrollTicking = false;
      });
      scrollTicking = true;
    }
  });

  // ---------- Mobile Menu Toggle ----------
  function toggleMenu() {
    hamburger.classList.toggle('active');
    folderTabs.classList.toggle('open');
  }

  function closeMenu() {
    hamburger.classList.remove('active');
    folderTabs.classList.remove('open');
  }

  hamburger.addEventListener('click', toggleMenu);

  // Close menu on link click
  folderTabs.querySelectorAll('.nav-link').forEach((link) => {
    link.addEventListener('click', closeMenu);
  });

  // ---------- Smooth Scroll for Nav Links ----------
  navAnchors.forEach((anchor) => {
    anchor.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = anchor.getAttribute('href');
      const targetEl = document.querySelector(targetId);

      if (targetEl) {
        const offsetTop =
          targetEl.getBoundingClientRect().top +
          window.scrollY -
          70; // nav height offset

        window.scrollTo({
          top: offsetTop,
          behavior: 'smooth',
        });
      }

      // Update active state
      navAnchors.forEach((a) => a.classList.remove('active'));
      anchor.classList.add('active');
    });
  });

  // ---------- Back to Top ----------
  backToTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // ---------- Active Nav on Scroll ----------
  const sections = document.querySelectorAll('section[id], header[id], footer[id]');

  const sectionObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const id = entry.target.getAttribute('id');
          navAnchors.forEach((a) => {
            a.classList.remove('active');
            if (a.getAttribute('href') === `#${id}`) {
              a.classList.add('active');
            }
          });
        }
      });
    },
    {
      threshold: 0.3,
      rootMargin: '-70px 0px -50% 0px',
    }
  );

  sections.forEach((section) => sectionObserver.observe(section));

  // ---------- Escape key closes menu ----------
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeMenu();
      closeDrawer();
    }
  });

  // ---------- File Cabinet Drawer ----------
  const drawerToggle = document.getElementById('pressDrawerToggle');
  const drawer = document.getElementById('pressDrawer');
  const drawerClose = document.getElementById('pressDrawerClose');

  function openDrawer() {
    drawer.classList.add('open');
    drawerToggle.setAttribute('aria-expanded', 'true');

    // Stagger card animations
    const cards = drawer.querySelectorAll('.file-card');
    cards.forEach((card, i) => {
      card.style.transitionDelay = `${0.3 + i * 0.02}s`;
    });

    // Scroll drawer into view after it opens
    setTimeout(() => {
      drawer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 400);
  }

  function closeDrawer() {
    drawer.classList.remove('open');
    drawerToggle.setAttribute('aria-expanded', 'false');

    // Reset delays
    const cards = drawer.querySelectorAll('.file-card');
    cards.forEach((card) => {
      card.style.transitionDelay = '0s';
    });
  }

  if (drawerToggle && drawer) {
    drawerToggle.addEventListener('click', (e) => {
      e.preventDefault();
      if (drawer.classList.contains('open')) {
        closeDrawer();
      } else {
        openDrawer();
      }
    });
  }

  if (drawerClose) {
    drawerClose.addEventListener('click', closeDrawer);
  }

  // Run initial scroll check
  handleNavScroll();
});
