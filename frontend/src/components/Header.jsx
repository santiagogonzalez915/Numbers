import numbersLogo from "../assets/numbers_logo.png";

export default function Header() {
  return (
    <header className="flex justify-center items-center">
      <img
        src={numbersLogo}
        alt="Numbers Game Logo"
        className="h-32 w-auto object-contain drop-shadow mb-0"
      />
    </header>
  );
}
