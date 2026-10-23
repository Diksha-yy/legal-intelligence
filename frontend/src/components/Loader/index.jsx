/**
 * Loader — a centered spinning ring used while waiting for API responses.
 * Use size="sm" for inline loaders, size="lg" for full-page blocks.
 */
function Loader({ size = "md", className = "" }) {
  const dims = {
    sm: "h-4 w-4 border-2",
    md: "h-8 w-8 border-4",
    lg: "h-12 w-12 border-4",
  };

  return (
    <div className={`flex items-center justify-center ${className}`}>
      <div
        className={`animate-spin rounded-full border-royal border-t-transparent ${dims[size]}`}
      />
    </div>
  );
}

export default Loader;
