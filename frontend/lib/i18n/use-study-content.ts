import { useTranslation } from "./context";
import { studyEn, studyRu, StudyContent } from "./study-content";

export function useStudyContent(): StudyContent {
  const { locale } = useTranslation();
  return locale === "ru" ? studyRu : studyEn;
}
