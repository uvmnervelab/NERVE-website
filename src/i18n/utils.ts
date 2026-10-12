import { ui, defaultLang } from './ui';

export function getLangFromUrl(url: URL) {
  const [, lang] = url.pathname.split('/');
  if (lang in ui) return lang as keyof typeof ui;
  return defaultLang;
}

export function useTranslations(lang: keyof typeof ui) {
  return function t(key: keyof typeof ui[typeof defaultLang]) {
    // Not every language defines every key; fall back to the default language.
    return (ui[lang] as Partial<Record<typeof key, string>>)[key] || ui[defaultLang][key];
  }
}
