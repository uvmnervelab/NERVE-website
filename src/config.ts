export const SITE = {
  website: 'https://nervelab.uvm.edu/', // Replace with your actual deployed URL
  author: 'NERVE Lab',
  description: 'Website for the Neuroimaging Research Vermont (NERVE) Lab at the University of Vermont.',
  title: 'NERVE Lab',
  ogImage: 'astropaper-og.jpg',
  lightAndDarkMode: true,
  postPerPage: 3,
  scheduledPostMargin: 15 * 60 * 1000, // 15 minutes

  // Lab Info
  labName: 'NERVE Lab',
  university: 'University of Vermont',
  logo: undefined as string | undefined, // Logo path, e.g. '/assets/logo-real.svg' (unset = no header logo)
  avatar: undefined as string | undefined, // Avatar for SEO/Schema (falls back to logo)
  email: 'nervelab@uvm.edu', // Contact email for Join Us page

  // Hero Section (Home Page)
  hero: {
    title: 'Studying Relationships Between Brain Development and Behavior.',
    subtitle: 'We are the NERVE Lab at the University of Vermont.',
    action: 'Publications', // Optional call to action text
    image: undefined, // Hero image path
  },

  // Navigation
  nav: [
    { text: 'Home', link: '/', key: 'home' },
    { text: 'Research', link: '/research', key: 'research' },
    { text: 'Publications', link: '/publications', key: 'publications' },
    { text: 'Team', link: '/team', key: 'team' },
    { text: 'News', link: '/news', key: 'news' },
    { text: 'Search', link: '/search', key: 'search' },
  ],

  // Custom Pages (Appended after 'Join Us')
  customPages: [] as { text: string; link: string; key: string }[],

  // i18n Config
  i18n: {
    enabled: false,
    defaultLocale: 'en',
  }
};

export const LOCALE = {
  lang: 'en', // html lang code. Set this empty and default will be "en"
  langTag: ['en-EN'], // BCP 47 Language Tags. Set this empty [] to use the environment default
} as const;

export const LOGO_IMAGE = {
  enable: true,
  svg: true,
  width: 216,
  height: 46,
};

export const SOCIALS = [
  {
    link: 'https://github.com/fjd2004711/scholar-lite',
    active: true,
  },
];

// Default language configuration
export const DEFAULT_LANG: 'zh' | 'en' | 'ja' | 'ko' | 'fr' | 'de' | 'es' | 'ru' = 'en';
