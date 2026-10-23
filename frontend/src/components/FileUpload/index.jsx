import { useRef, useState } from "react";
import { UploadCloud } from "lucide-react";
import { useLanguage } from "../../i18n/LanguageContext";

// Drag-and-drop file dropzone used on the Document Upload page.
// Calls onFileSelected(file) as soon as a file is dropped or chosen.
function FileUpload({ onFileSelected, accept = ".pdf,.jpg,.jpeg,.png" }) {
  const { t } = useLanguage();
  const inputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);

  function handleFiles(fileList) {
    const file = fileList?.[0];
    if (file) onFileSelected?.(file);
    if (inputRef.current) inputRef.current.value = "";
  }

  return (
    <div
      role="button"
      tabIndex={0}
      aria-label={t("fileUpload.accessible")}
      onDragOver={(e) => {
        e.preventDefault();
        setIsDragging(true);
      }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={(e) => {
        e.preventDefault();
        setIsDragging(false);
        handleFiles(e.dataTransfer.files);
      }}
      onKeyDown={(e) => {
        if (e.target !== e.currentTarget || !["Enter", " "].includes(e.key)) return;
        e.preventDefault();
        inputRef.current?.click();
      }}
      onClick={() => inputRef.current?.click()}
      className={`group flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed px-6 py-16 text-center transition-[transform,border-color,background-color,box-shadow] duration-200 ease-out hover:-translate-y-0.5 hover:shadow-lg hover:shadow-royal/5 motion-reduce:transform-none motion-reduce:transition-none ${
        isDragging
          ? "border-royal bg-royal/5"
          : "border-slate-300 bg-white hover:border-royal/50"
      }`}
    >
      <span className="flex h-14 w-14 items-center justify-center rounded-xl bg-royal/10 text-royal transition-[transform,background-color,color] duration-200 group-hover:scale-105 group-hover:bg-royal group-hover:text-white group-focus-visible:scale-105 motion-reduce:transform-none motion-reduce:transition-none">
        <UploadCloud size={22} />
      </span>

      <p className="mt-4 font-semibold text-navy">
        {t("fileUpload.drop")}
      </p>
      <p className="mt-1 text-sm text-slate-500">
        {t("fileUpload.browse")}
      </p>

      <span className="mt-5 inline-flex items-center justify-center gap-2 rounded-2xl bg-royal px-6 py-3.5 text-base font-semibold text-white shadow-lg shadow-royal/25">
        <UploadCloud size={16} /> {t("fileUpload.choose")}
      </span>

      <input
        ref={inputRef}
        type="file"
        accept={accept}
        className="hidden"
        onChange={(e) => handleFiles(e.target.files)}
      />
    </div>
  );
}

export default FileUpload;
