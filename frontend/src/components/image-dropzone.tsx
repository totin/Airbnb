import { useRef, useState } from "react";
import { ImagePlus, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const MAX_MB = 5;

function leerArchivo(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result));
    reader.onerror = () => reject(new Error("No se pudo leer la imagen"));
    reader.readAsDataURL(file);
  });
}

/** Recuadro para arrastrar y soltar (o elegir) fotos de la propiedad. */
export function ImageDropzone({
  imagenes,
  onChange,
  max = 8,
}: {
  imagenes: string[];
  onChange: (imgs: string[]) => void;
  max?: number;
}) {
  const [dragging, setDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const agregar = async (files: FileList | null) => {
    if (!files?.length) return;
    setError(null);
    const validos = Array.from(files).filter((f) => f.type.startsWith("image/"));
    if (validos.length !== files.length) setError("Solo se aceptan imágenes");
    const pesados = validos.filter((f) => f.size > MAX_MB * 1024 * 1024);
    if (pesados.length) setError(`Cada imagen debe pesar menos de ${MAX_MB} MB`);
    const ok = validos.filter((f) => f.size <= MAX_MB * 1024 * 1024).slice(0, max - imagenes.length);
    const dataUrls = await Promise.all(ok.map(leerArchivo));
    onChange([...imagenes, ...dataUrls]);
  };

  return (
    <div className="space-y-3">
      <div
        role="button"
        tabIndex={0}
        onClick={() => inputRef.current?.click()}
        onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && inputRef.current?.click()}
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragging(false);
          void agregar(e.dataTransfer.files);
        }}
        className={cn(
          "flex cursor-pointer flex-col items-center justify-center gap-2 rounded-lg border-2 border-dashed border-border p-8 text-center transition-colors",
          dragging ? "border-primary bg-primary/5" : "hover:bg-secondary",
        )}
      >
        <ImagePlus className="size-6 text-muted-foreground" />
        <p className="text-sm font-medium">Arrastrá las fotos de tu propiedad acá</p>
        <p className="text-xs text-muted-foreground">
          o hacé clic para elegirlas · hasta {max} imágenes de {MAX_MB} MB
        </p>
        <input
          ref={inputRef}
          type="file"
          accept="image/*"
          multiple
          className="hidden"
          onChange={(e) => {
            void agregar(e.target.files);
            e.target.value = "";
          }}
        />
      </div>

      {error && <p className="text-sm text-destructive">{error}</p>}

      {imagenes.length > 0 && (
        <div className="grid grid-cols-3 gap-2 sm:grid-cols-4">
          {imagenes.map((src, i) => (
            <div key={`${i}-${src.slice(-16)}`} className="group relative overflow-hidden rounded-md">
              <img
                src={src}
                alt={`Foto ${i + 1} de la propiedad`}
                loading="lazy"
                className="aspect-4/3 w-full object-cover"
              />
              <Button
                type="button"
                size="icon"
                variant="secondary"
                aria-label={`Quitar foto ${i + 1}`}
                onClick={() => onChange(imagenes.filter((_, j) => j !== i))}
                className="absolute right-1 top-1 size-6 rounded-full"
              >
                <X className="size-3.5" />
              </Button>
              {i === 0 && (
                <span className="absolute bottom-1 left-1 rounded bg-background/80 px-1.5 py-0.5 text-[10px] font-medium">
                  Portada
                </span>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
