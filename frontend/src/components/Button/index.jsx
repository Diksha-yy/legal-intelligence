import "./button.css";

function Button({
  children,
  variant = "primary",
  size = "medium",
  onClick,
  type = "button",
}) {
  return (
    <button
      className={`btn ${variant} ${size}`}
      onClick={onClick}
      type={type}
    >
      {children}
    </button>
  );
}

export default Button;